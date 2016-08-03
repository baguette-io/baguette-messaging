#-*- coding:utf-8 -*-
"""
Module containing all the croissant mixins.
"""
import abc
import contextlib
import croissant.settings

class EntryPointMixin(object):
    """
    | Entry point Mixin.
    | All services that are listening for an event(like a consumer, an http server, ...)
    | are called `Entry Point` and then must inherit from it.
    | They will implement debug mode, monitoring, etc.
    """
    __metaclass__ = abc.ABCMeta

    callback = None

    def main_callback(self, *args, **kwargs):
        """
        Main callback called when an event is received from an entry point.

        :returns: The entry point's callback.
	:rtype: function
        :raises NotImplementedError: When the entrypoint doesn't have the required attributes.
        """
        if not self.callback:
            raise NotImplementedError('Entrypoints must declare `callback`')
        if not self.settings:
            raise NotImplementedError('Entrypoints must declare `settings`')

        #1. Start all the middlewares
        with self.debug(*args, **kwargs):
            #2. `Real` callback
            result = self.callback(*args, **kwargs)#pylint: disable=not-callable
        return result

    @abc.abstractmethod
    def debug(self):
        """
        | The debug implementation for the entry point,
        | Each entry point must have it's own debug logic.
        """
