#-*- coding:utf-8 -*-
"""
Dummy class that execute a method.
"""
import contextlib
import farine.settings
from farine.mixins import EntryPointMixin

class Method(EntryPointMixin):
    """
    Execute the method.
    """

    def __init__(self, *args, **kwargs):#pylint:disable=unused-argument
        """
        :param service: The service's name which execute the method.
        :type service: str
        :param callback: The method to call.
        :type callback: object
        :rtype: None
        """
        self.callback = kwargs.get('callback')
        self.service = kwargs.get('service')
        self.settings = getattr(farine.settings, self.service)

    @contextlib.contextmanager
    def debug(self):#pylint:disable=arguments-differ,unused-argument
        """
        Add a debug method.
        """
        yield

    def run(self, restart):
        """
        Execute the method.
        :param restart: Restart the method if it ends.
        :type restart: bool
        :rtype: None
        """
        while True:
            result = self.main_callback()
            if not restart:
                break
        return result

    def start(self, *args, **kwargs):#pylint:disable=unused-argument
        """
        Launch the method.
        :param restart: Restart the method if it ends.
        :type restart: bool
        :rtype: None
        """
        restart = kwargs.get('restart', True)
        return self.run(restart)

    def stop(self):
        """
        Stop the execution.
        :rtype: None
        """
