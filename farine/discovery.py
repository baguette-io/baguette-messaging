#-*- coding:utf-8 -*-
"""
| Module containing everything related to service management:
| Register services to launch, start them.


|TODO: J'en ai vu de la merde, mais de la merde comme ca. CLEANUP.
"""
import inspect
import logging
import sys
import gevent.threadpool
LOGGER = logging.getLogger(__name__)


ENTRYPOINTS = [] #List of a tuple: (Entrypoint, callback, args, kwargs)

def import_module(module):
    """
    | Given a module `service`, try to import it.
    | It will autodiscovers all the entrypoints
    | and add them in `ENTRYPOINTS`.

    :param module: The module's name to import.
    :type module: str
    :rtype: None
    :raises ImportError: When the service/module to start is not found.
    """
    try:
        __import__('{0}.service'.format(module))
    except ImportError:
        LOGGER.error('No module/service found. Quit.')
        sys.exit(0)

def start():
    """
    | Start all the registered entrypoints
    | that have been added to `ENTRYPOINTS`.

    :rtype: None
    """
    pool = gevent.threadpool.ThreadPool(len(ENTRYPOINTS))
    for entrypoint, callback, args, kwargs in ENTRYPOINTS:
        cname = callback.__name__
        #1. Retrieve the class which owns the callback
        for name, klass in inspect.getmembers(sys.modules[callback.__module__], inspect.isclass):
            if hasattr(klass, cname):
                service_name = name.lower()
                break
        #2.Start the entrypoint
        callback = getattr(klass(), cname)
        kwargs.update({'service':service_name, 'callback':callback, 'callback_name': cname})
        LOGGER.info('Start service %s[%s].', service_name.capitalize(), cname)
        obj = entrypoint(*args, **kwargs)
        pool.spawn(obj.start, *args, **kwargs)
    pool.join()
    return True
