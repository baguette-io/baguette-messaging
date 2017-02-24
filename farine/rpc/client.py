#-*- coding:utf-8 -*-
"""
RPC over AMQP implementation: client side.
"""
import uuid
from kombu import Connection, Producer, Queue

import farine.amqp

class Client(farine.amqp.Consumer):
    """
    RPC Client which is
    an AMQP publisher then consumer.
    """
    prefetch_count = 1
    exclusive = True
    auto_delete = True
    auto_generated = True
    timeout = 10

    def __getattr__(self, method, *args, **kwargs):
        self.method = method
        return self.__rpc__

    def __rpc__(self, *args, **kwargs):
        self.response = None
        self.correlation_id = uuid.uuid4().hex
        message = {'args': args,
                   'kwargs': kwargs
        }
        publish = farine.amqp.Publisher(self.service, '{}__{}'.format(self.service, self.method))
        publish.send(message,
            correlation_id=self.correlation_id,
            reply_to=self.queue.name
        )
        self.start(forever=False, timeout=self.timeout)
        return self.response

    def callback(self, result, message):
        message.ack()
        self.response = result
