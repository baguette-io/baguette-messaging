#-*- coding:utf-8 -*-
"""
Module containing the class decorators:
 * publish()
 * consume()
"""
import logging
import farine.discovery
from farine.amqp.publisher import Publisher
from farine.amqp.consumer import Consumer

LOGGER = logging.getLogger(__name__)

def publish(exchange=None, routing_key=None):
    def wrapper(method):
        def subwrapper(self, *args, **kwargs):
            if not hasattr(self, 'publish'):
                name = getattr(self, 'service', self.__class__.__name__.lower())
                _routing_key = routing_key or kwargs.get('routing_key') or name
                if kwargs.get('routing_key'):
                    kwargs.pop('routing_key')
                publish = Publisher(exchange or name, _routing_key, service=name)
            return method(self, publish, *args, **kwargs)
        return subwrapper
    return wrapper

def consume(*args, **kwargs):
    def wrapper(method):
        farine.discovery.ENTRYPOINTS.append((Consumer, method, args, kwargs))
        def subwrapper(self, *args, **kwargs):
            LOGGER.info('Received message : %s %s , call %s.', args, kwargs, method.__name__)
            return method(self, *args, **kwargs)
        return subwrapper
    return wrapper
