#-*- coding:utf-8 -*-
"""
Module containing a consumer
to a stream HTTP Connection.
"""
import contextlib
import farine.settings
import farine.utils as utils
from farine.mixins import EntryPointMixin
import sseclient

class SSEConsumer(EntryPointMixin):
    """
    HTTP SSE consumer.
    """

    def __init__(self, *args, **kwargs):#pylint:disable=unused-argument
        """
        :param service: The service's name which consume the stream.
        :type service: str
        :param callback: The callback to call when receiving a message.
        :type callback: object
        :rtype: None
        """
        self.callback = kwargs.get('callback')
        self.service = kwargs.get('service')
        self.settings = getattr(farine.settings, self.service)
        self.endpoint = kwargs.get('endpoint', self.settings['endpoint'])
        self.headers = kwargs.get('headers', {'Accept':'text/event-stream'})
        self.stream = None


    @contextlib.contextmanager
    def debug(self, data):#pylint:disable=arguments-differ,unused-argument
        """
        Add a debug method.
        """
        yield

    def run(self, limit=None, timeout=None):
        """
        Consume the event stream.
        :param timeout: Duration of the connection timeout.
        :type timeout: int
        :param limit: Number of events to consume.
        :type limit: int
        :rtype: None
        """
        counter = 0
        self.stream = sseclient.SSEClient(self.endpoint)
        while True:
            with utils.Timeout(timeout):
                try:
                    event = next(self.stream)
                except StopIteration:
                    continue
                else:
                    if not event.data:
                        continue
                    self.main_callback(event.data)
                    counter += 1
                    if limit and counter >= limit:
                        return

    def start(self, *args, **kwargs):#pylint:disable=unused-argument
        """
        | Launch the SSE consumer.
        | It can listen forever for messages or just wait for one.

        :param limit: If set, the consumer listens for a limited number of events.
        :type limit: int
        :param timeout: If set, the consumer listens for an event for a limited time.
        :type timeout: int
        :rtype: None
        """
        limit = kwargs.get('limit', None)
        timeout = kwargs.get('timeout', None)
        self.run(limit=limit, timeout=timeout)

    def stop(self):
        """
        Stop the consumer.
        :rtype: None
        """
