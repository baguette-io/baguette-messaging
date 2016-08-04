#-*- coding:utf-8 -*-
import json
from fixtures import *
from farine.amqp import Consumer
from pytest_dbfixtures import factories
from pytest_dbfixtures.factories.rabbitmq_client import clear_rabbitmq

def test_no_has_publish(publisher_factory):
    publisher = publisher_factory()
    assert hasattr(publisher, 'publish') ==  False

def test_exchange_created(rabbitmq, publisher_factory, rabbitmq_proc):
    publisher = publisher_factory()
    assert 'publish' not in rabbitmq_proc.list_exchanges()
    assert publisher.publish_dummy({'test':'ok'})
    assert 'publish' in rabbitmq_proc.list_exchanges()
    clear_rabbitmq(rabbitmq_proc, rabbitmq)

def test_message_sent(publisher_factory, queue_factory, rabbitmq_proc, rabbitmq):
    queue = queue_factory('consume', 'publish', 'publish')
    publisher = publisher_factory()
    publisher.publish_dummy({'test':'ok'})
    message = next(queue.consume())
    assert json.loads(message.body) == {"test": "ok"}
    clear_rabbitmq(rabbitmq_proc, rabbitmq)

def test_consumer_read(queue_factory, rabbitmq_proc, rabbitmq, consumer_factory, publisher_factory):
    queue = queue_factory('consume', 'publish', 'publish')
    consumer = consumer_factory()
    worker_consumer = Consumer(exchange='publish', routing_key='publish', service='consume', callback=consumer.consume_dummy)
    publisher_factory().publish_dummy({'test':'ok'})
    #
    worker_consumer.start(forever=False)
    assert 'consume' in rabbitmq_proc.list_queues()
    assert consumer.messages_consumed == 1
    clear_rabbitmq(rabbitmq_proc, rabbitmq)

def test_debug(queue_factory, rabbitmq_proc, rabbitmq, consumer_factory, publisher_factory):
    queue = queue_factory('consume', 'publish', 'publish')
    consumer = consumer_factory()
    worker_consumer = Consumer(exchange='publish', routing_key='publish', service='consume', callback=consumer.consume_dummy)
    publisher_factory().publish_dummy({'test':'ok', '__debug__':True})
    worker_consumer.start(forever=False)
    #Check that the queue debug auto created has one message
    debug = queue_factory('debug', 'publish', 'debug')
    debug_msg = json.loads(next(debug.consume()).body)
    assert '__debug__' in debug_msg.keys()
    clear_rabbitmq(rabbitmq_proc, rabbitmq)
