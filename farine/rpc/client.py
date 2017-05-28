#-*- coding:utf-8 -*-
#pylint:disable=attribute-defined-outside-init,method-hidden
"""
RPC over AMQP implementation: client side.
"""
import uuid
import traceback

import farine.amqp
import farine.exceptions as exceptions

class Client(farine.amqp.Consumer):
    """
    RPC Client which is
    an AMQP publisher then consumer.
    """
    prefetch_count = 1
    exclusive = True
    auto_delete = True
    auto_generated = True

    def __init__(self, service, timeout=None):
        super(Client, self).__init__(service, service, service=service)
        self.timeout = timeout

    def __getattr__(self, method, *args, **kwargs):
        self.method = method
        return self.__rpc__

    def __rpc__(self, *args, **kwargs):
        self.response = {'__except__': None, 'body': None}
        self.correlation_id = uuid.uuid4().hex
        stream = kwargs['__stream__'] = kwargs.get('__stream__', False)
        message = {'args': args,
                   'kwargs': kwargs
                  }
        publish = farine.amqp.Publisher(self.service, '{}__{}'.format(self.service, self.method))
        publish.send(message,
                     correlation_id=self.correlation_id,
                     reply_to=self.queue.name
                    )
        run = True
        while run:
            try:
                self.start(forever=False, timeout=self.timeout)
            except:#pylint:disable=bare-except
                self.response['__except__'] = traceback.format_exc()

            if self.response['__except__']:
                raise exceptions.RPCError(self.response['__except__'])
            if not stream:
                run = False
                return self.response['body']

    def callback(self, result, message):
        """
        Method called automatically when a message is received.
        This will be executed before exiting self.start().
        """
        message.ack()
        self.response['body'] = result
        self.response['__except__'] = result.get('__except__', None)
