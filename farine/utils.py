#-*- coding:utf-8 -*-
"""
Utils containing useful tools.
"""
import contextlib
import signal
import logging
import farine.exceptions as exceptions

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



class Timeout(object):
    """
    Dummy timeout context manager.
    """

    def __init__(self, seconds):
        """
        :param seconds: the timeout must be specified in seconds.
        :type seconds: int
        """
        self.seconds = seconds

    def handler(self, signum, frame):
        """
        Handler of the timeout.
        """
        raise exceptions.TimeoutError('{0} seconds reached.'.format(self.seconds))

    def __enter__(self):
        """
        Create a timeout if seconds is specified.
        """
        if self.seconds:
            signal.signal(signal.SIGALRM, self.handler)
            signal.alarm(self.seconds)

    def __exit__(self, type, value, traceback):
        """
        Deactivate the timeout.
        """
        if self.seconds:
            signal.alarm(0)
