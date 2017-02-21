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

    def __getattr__(self, method, *args, **kwargs):
        print '__getattr__'
        print method
        print args
        print kwargs
        return self.__call__(method, *args, **kwargs)

    def __call__(self, method, *args, **kwargs):
        print '__call__'
        print 'method : {}'.format(method)
        print args
        print kwargs
        self.correlation_id = uuid.uuid4().hex
        message = {'method' : method,
                   'args': args,
                   'kwargs': kwargs
        }
        publish = farine.amqp.Publisher(self.service, self.routing_key)
        publish(message,
                correlation_id=self.correlation_id,
                reply_to=self.queue
        )
        self.start(forever=False)

    def __callback__(self, body, message, publish):
        print 'CLIENT.CALLBACK'
        print body
        print message
        result = {}
        message.ack()
        return 
