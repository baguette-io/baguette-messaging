#-*- coding:utf-8 -*-
"""
Module containing the class decorators:
 * http()
"""
import logging
import farine.discovery
from farine.stream.sse import SSEConsumer

LOGGER = logging.getLogger(__name__)

def http(*args, **kwargs):
    def wrapper(_method):
        farine.discovery.ENTRYPOINTS.append((SSEConsumer, _method, args, kwargs))
        def subwrapper(self, *args, **kwargs):
            LOGGER.info('Received message : %s %s , call %s.', args, kwargs, _method.__name__)
            return _method(self, *args, **kwargs)
        return subwrapper
    return wrapper
