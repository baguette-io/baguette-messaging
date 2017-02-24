#-*- coding:utf-8 -*-
import multiprocessing
import time
import pytest
import farine.amqp
import farine.log
import farine.rpc
import farine.rpc as rpc
import farine.settings
import kombu.log
from rabbitpy import Exchange, Queue, Message
from pytest_rabbitmq.factories.client import clear_rabbitmq

@pytest.fixture(autouse=True)
def settings():
    farine.settings.load()

@pytest.fixture(autouse=True)
def logging():
    farine.log.setup_logging(__name__, False)
    kombu.log.setup_logging(loglevel='DEBUG')

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

    def exception(self, *args, **kwargs):
        return i_am_broken

class Client(object):
    @rpc.client('server')
    def call(self, rpc):
        result = rpc.something('un', deux='deux')
        return result

    @rpc.client('server')
    def call_exception(self, rpc):
        try:
            rpc.exception()
            return True
        except farine.rpc.RPCError:
            return False

def _rpc_server(callback_name):
    server = Server()
    farine.settings.load()
    rpc.Server(service='server', callback_name=callback_name, callback=getattr(server, callback_name)).start()

@pytest.fixture()
def rpc_server_factory(request, rabbitmq_proc, rabbitmq):
    def factory(callback_name):
        process = multiprocessing.Process(
            target=lambda:_rpc_server(callback_name),
        )
        def cleanup():
            process.terminate()
            clear_rabbitmq(rabbitmq_proc, rabbitmq)
        request.addfinalizer(cleanup)
        process.start()
        time.sleep(5)
        return process
    return factory

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
