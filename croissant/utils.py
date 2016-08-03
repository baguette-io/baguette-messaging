#-*- coding:utf-8 -*-
"""
Utils containing
useful little functions.
"""
import contextlib
import logging

LOGGER = logging.getLogger(__name__)

@contextlib.contextmanager
def suppress(*exceptions):
    """
    | Log and ignore `exceptions`.
    | If another exception occurs, it will be raised.

    :param exceptions: Exceptions to handle.
    :type exceptions: tuple
    :rtype: None
    """
    try:
        yield
    except exceptions as exc:
        LOGGER.error('Error occured, ignore it :%s.', exc)
