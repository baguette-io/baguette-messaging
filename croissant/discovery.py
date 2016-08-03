#-*- coding:utf-8 -*-
"""
| Module containing everything related to service management:
| Register services to launch, start them.


|TODO: J'en ai vu de la merde, mais de la merde comme ca. CLEANUP.
"""
import inspect
import logging
import sys
import gevent.pool
LOGGER = logging.getLogger(__name__)


ENTRYPOINTS = [] #List of a tuple: (Entrypoint, callback, args, kwargs)

def import_module(name):
    """
    | Given a module `name`, try to import it.
    | It will autodiscovers all the entrypoints
    | and add them in `ENTRYPOINTS`.

    :param name: The module's name to import.
    :type name: str
    :rtype: None
    :raises ImportError: When the module to start is not found.
    """
    sys.path.insert(0, '.')
    try:
        __import__(name)
    except ImportError:
        LOGGER.error('No module found. Quit.')
        sys.exit(0)

def start():
    """
    | Start all the registered entrypoints
    | that have been added to `ENTRYPOINTS`.

    :rtype: None
    """
    pool = gevent.pool.Pool()
    for entrypoint, callback, args, kwargs in ENTRYPOINTS:
        #1. Retrieve the class which owns the callback
        for name, klass in inspect.getmembers(sys.modules[callback.__module__], inspect.isclass):
            if hasattr(klass, callback.__name__):
                service_name = name.lower()
                break
        #2.Start the entrypoint
        kwargs.update({'service':service_name, 'callback':callback})
        LOGGER.info('Start service %s[%s].', service_name.capitalize(), callback.__name__)
        obj = entrypoint(*args, **kwargs)
        pool.spawn(obj.start, *args, **kwargs)
    pool.join()
    return True
