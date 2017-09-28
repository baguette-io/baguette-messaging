#-*- coding:utf-8 -*-
"""
Module containing all the farine mixins.
"""
import abc
import contextlib
import farine.connectors.sql as sql

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

        self.callback.im_self.db = None

        #1. Start all the middlewares
        with self.debug(*args, **kwargs):
            #2. `Real` callback
            with self.database():
                result = self.callback(*args, **kwargs)#pylint: disable=not-callable
        return result

    @abc.abstractmethod
    def debug(self):
        """
        | The debug implementation for the entry point,
        | Each entry point must have it's own debug logic.
        """

    @contextlib.contextmanager
    def database(self):
        """
        Before the callback is called, initialize the database if needed.
        :rtype: None
        """
        #1. Initialize
        self.callback.im_self.db = sql.setup(self.settings)
        print self.callback.__dict__
        print dir(self.callback)
        if self.callback.im_self.db:
            sql.init(self.callback.__module__, self.callback.im_self.db)
            self.callback.im_self.db.connect()
        yield
        #2. Cleanup
        if self.callback.im_self.db:
            self.callback.im_self.db.close()
