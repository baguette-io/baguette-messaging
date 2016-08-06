#-*- coding:utf-8 -*-
import pytest
import farine.amqp
import farine.log
import farine.settings
import kombu.log
from rabbitpy import Exchange, Queue, Message

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

@pytest.fixture()
def channel(rabbitmq):
    return rabbitmq.channel()

@pytest.fixture
def queue_factory(rabbitmq, rabbitmq_proc):
    def factory(name, exchange, routing_key):
        channel = rabbitmq.channel()
        exchange = Exchange(channel, exchange, durable=True)
        exchange.declare()
        queue = Queue(channel, name, durable=True)
        queue.declare()
        queue.bind(exchange, routing_key=routing_key)
        assert name in rabbitmq_proc.list_queues()
        return queue
    return factory

@pytest.fixture
def message():
    """
    Message factory.
    """
    def factory(exchange, routing_key, message, channel):
        message = Message(channel, message)
        return message.publish(exchange, routing_key)
    return factory

@pytest.fixture()
def amqp_factory():
    def factory(exchange, routing_key, name, callback):
        return farine.amqp.Consumer(exchange=exchange, routing_key=routing_key, service=name, callback=callback)
