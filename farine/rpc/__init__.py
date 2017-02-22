#-*-coding:utf-8 -*-
"""
Module containing the class decorators:
 * client()
 * method()
"""
import logging
import farine.discovery
from farine.rpc.client import Client
from farine.rpc.server import Server

LOGGER = logging.getLogger(__name__)

def client(service, exchange=None, routing_key=None):
    def wrapper(_method):
        def subwrapper(self, *args, **kwargs):
            _exchange = exchange or service
            _routing_key = routing_key or service
            if not hasattr(self, 'rpc'):
                rpc = Client(_exchange, _routing_key, service=service)
            return _method(self, rpc, *args, **kwargs)
        return subwrapper
    return wrapper

def method(*args, **kwargs):
    def wrapper(_method):
        farine.discovery.ENTRYPOINTS.append((Server, _method, args, kwargs))
        def subwrapper(self, *args, **kwargs):
            LOGGER.info('Received message : %s %s , call %s.', args, kwargs, _method.__name__)
            return _method(self, *args, **kwargs)
        return subwrapper
    return wrapper
