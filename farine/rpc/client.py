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
    auto_generated = True
    #TODO: delete the queue when the rpc call is done.
    #auto_delete = True
    #exclusive = True

    def __init__(self, service, timeout=None):
        super(Client, self).__init__(service, service, service=service)
        self.timeout = timeout
        self.remote = None

    def callback(self, result, message):
        """
        Method called automatically when a message is received.
        This will be executed before exiting self.start().
        """
        message.ack()
        self.response['body'] = result.get('body')
        self.response['__except__'] = result.get('__except__')
        self.response['__stream_end__'] = result.get('__stream_end__', False)

    def __wrap_rpc__(self, *args, **kwargs):
        """
        | Wrapper for our RPC method:
        | if it's a non streaming call, then we return the next and only one element of the generator.
        | Otherwise we returns the generator.
        """
        stream = kwargs.get('__stream__', False)
        result = self.__rpc__(*args, **kwargs)
        if stream:
            return result
        return next(result)


    def __rpc__(self, *args, **kwargs):
        """
        RPC call logic.
        There are two types of rpc calls:
        Streaming and basic.
        We don't set the auto_delete flag to the queue because of the streaming call.
        """
        self.correlation_id = uuid.uuid4().hex
        message = {'args': args,
                   'kwargs': kwargs
                  }
        publish = farine.amqp.Publisher(self.service, '{}__{}'.format(self.service, self.remote))
        publish.send(message,
                     correlation_id=self.correlation_id,
                     reply_to=self.queue.name
                    )
        run = True
        while run:
            try:
                self.response = {'__except__': None, '__stream_end__': False, 'body': None}
                self.start(forever=False, timeout=self.timeout)
            except:#pylint:disable=bare-except
                self.response['__except__'] = traceback.format_exc()

            if self.response['__except__']:
                raise exceptions.RPCError(self.response['__except__'])
            #1. If if it's not a streaming call, stop the loop and yield the response
            if not kwargs.get('__stream__', False):
                run = False
                yield self.response['body']
            #2. If it's the end of the streaming call, stop the loop
            elif self.response['__stream_end__']:
                run = False
            #3. If the streaming call is not done, just yield if we got an answer
            elif self.response['body'] is not None:
                yield self.response['body']


    def __getattr__(self, method, *args, **kwargs):
        self.remote = method
        return self.__wrap_rpc__
