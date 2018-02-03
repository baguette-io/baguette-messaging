#-*-coding:utf-8 -*-
"""
Module containing the class decorators:
 * method()
"""
import logging
import farine.discovery
from farine.execute.method import Method

LOGGER = logging.getLogger(__name__)
def method(*args, **kwargs):
    def wrapper(_method):
        farine.discovery.ENTRYPOINTS.append((Method, _method, args, kwargs))
        def subwrapper(self, *args, **kwargs):
            return _method(self, *args, **kwargs)
        return subwrapper
    return wrapper
