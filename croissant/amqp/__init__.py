#-*- coding:utf-8 -*-
"""
Module containing the class decorators:
 * publish()
 * consume()
"""
import logging
import croissant.discovery
from croissant.amqp.publisher import Publisher
from croissant.amqp.consumer import Consumer

LOGGER = logging.getLogger(__name__)

def publish(exchange=None, routing_key=None):
    def wrapper(method):
        def subwrapper(self, *args, **kwargs):
            if not hasattr(self, 'publish'):
                name = self.__class__.__name__.lower()
                publish = Publisher(exchange or name, routing_key or name)
            return method(self, publish, *args, **kwargs)
        return subwrapper
    return wrapper

def consume(*args, **kwargs):
    def wrapper(method):
        croissant.discovery.ENTRYPOINTS.append((Consumer, method, args, kwargs))
        def subwrapper(self, *args, **kwargs):
            LOGGER.info('Received message : %s %s , call %s.', args, kwargs, method.__name__)
            return method(self, *args, **kwargs)
        return subwrapper
    return wrapper
