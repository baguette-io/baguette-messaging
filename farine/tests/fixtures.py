#-*- coding:utf-8 -*-
import multiprocessing
import time
import pytest
import farine.amqp
import farine.log
import farine.exceptions as exceptions
import farine.rpc as rpc
import farine.stream as stream
import farine.execute as execute
import farine.settings
import kombu.log
import requests
import requests_mock
from rabbitpy import Exchange, Queue, Message
from pytest_rabbitmq.factories.client import clear_rabbitmq
from .models import User

@pytest.fixture(autouse=True)
def settings():
    farine.settings.load()

@pytest.fixture(autouse=True)
def logging():
    farine.log.setup_logging(__name__, False)
    kombu.log.setup_logging(loglevel='INFO')

class Publish(object):

    @farine.amqp.publish()
    def publish_dummy(self, publish, message):
        publish(message)
        return True

class Consume(object):
    messages_consumed = 0

    @farine.amqp.consume(exchange='publish', routing_key='publish', forever=False)
    def consume_dummy(self, body, message):
        self.messages_consumed += 1
        return True

@pytest.fixture()
def publisher_factory():
    return Publish

@pytest.fixture()
def consumer_factory():
    return Consume

class Server(object):
    @rpc.method()
    def something(self, *args, **kwargs):
        return True

    @rpc.method()
    def exception(self, *args, **kwargs):
        return i_am_broken

    @rpc.method()
    def slow(self, *args, **kwargs):
        time.sleep(60)
        return True

    @rpc.method()
    def stream(self, *args, **kwargs):
        yield 'a'
        yield 'b'
        yield 'c'

class Model(object):
    @rpc.method()
    def save(self, name):
        with self.db.transaction() as txn:
            User.create(name=name)
            txn.commit()
        return True

    @rpc.method()
    def get(self):
        return User.select().count()

class Client(object):
    @rpc.client('server', 40)
    def call(self, rpc):
        result = rpc.something('un', deux='deux')
        return result

    @rpc.client('server', 40)
    def call_exception(self, rpc):
        try:
            rpc.exception()
            return True
        except exceptions.RPCError:
            return False

    @rpc.client('model', 40)
    def save(self, rpc, name):
        return rpc.save(name)

    @rpc.client('model', 40)
    def get(self, rpc):
        return rpc.get()


def _rpc_server(callback_name, service='server'):
    callbacks = {'server': Server, 'model': Model}
    farine.settings.load()
    rpc.Server(service=service, callback_name=callback_name, callback=getattr(callbacks[service](), callback_name)).start()

@pytest.fixture()
def rpc_server_factory(request, rabbitmq_proc, rabbitmq):
    def factory(callback_name, service='server'):
        process = multiprocessing.Process(
            target=lambda:_rpc_server(callback_name, service),
        )
        def cleanup():
            process.terminate()
            clear_rabbitmq(rabbitmq_proc, rabbitmq)
        request.addfinalizer(cleanup)
        process.start()
        time.sleep(5)
        return process
    return factory

class StreamSSEClient(object):
    messages_consumed = 0

    @stream.http()
    def event(self, data):
        self.messages_consumed += 1
        return data

@pytest.fixture()
def sse_client_factory():
    return StreamSSEClient

@pytest.fixture()
def sse_server_ok():
    with requests_mock.mock() as m:
        text = """event: event_stream_detached
data: {"remoteAddress":"10.1.0.234","eventType":"event_stream_detached","timestamp":"2017-05-25T17:27:08.373Z"}\n\n"""
        m.get('http://unittest/v2/events', text=text)
        yield

class ExecuteMethodClient(object):
    @execute.method()
    def mymethod(self):
        return 'executed'

@pytest.fixture()
def execute_client_factory():
    return ExecuteMethodClient

@pytest.fixture()
def rpc_client_factory():
    return Client

@pytest.fixture()
def channel(rabbitmq):
    return rabbitmq.channel()

@pytest.fixture
def queue_factory(rabbitmq, rabbitmq_proc):
    def factory(name, exchange, routing_key):
        channel = rabbitmq.channel()
        exchange = Exchange(channel, exchange, auto_delete=False, durable=True)
        exchange.declare()
        assert exchange.name in rabbitmq_proc.list_exchanges()
        queue = Queue(channel, name, auto_delete=False, durable=True)
        queue.declare()
        queue.bind(exchange, routing_key=routing_key)
        assert name in rabbitmq_proc.list_queues()
        return exchange, queue
    return factory

@pytest.fixture
def message_factory():
    """
    Message factory.
    """
    def factory(service, routing_key, message):
        pub = farine.amqp.Publisher(service, routing_key)
        return pub.send(message)
    return factory

@pytest.fixture()
def amqp_factory(request, rabbitmq_proc, rabbitmq):
    def factory(exchange, routing_key, name, callback, queue_name=None):
        return farine.amqp.Consumer(exchange=exchange, routing_key=routing_key,
            service=name, callback=callback, queue_name=queue_name)
    def cleanup():
        clear_rabbitmq(rabbitmq_proc, rabbitmq)
    request.addfinalizer(cleanup)
    return factory
