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

def client(service, timeout=None):
    def wrapper(_method):
        def subwrapper(self, *args, **kwargs):
            if not hasattr(self, 'rpc'):
                rpc = Client(service, timeout)
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
