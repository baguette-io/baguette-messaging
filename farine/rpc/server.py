#-*- coding:utf-8 -*-
"""
RPC over AMQP implementation: server side.
"""
import types
import traceback
import farine.amqp

class Server(farine.amqp.Consumer):
    """
    RPC Server which is
    an AMQP consumer then producer.
    """
    prefetch_count = 1
    routing_key_format = '{service}__{callback_name}'

    @farine.amqp.publish()
    def main_callback(self, publish, result, message):#pylint:disable=arguments-differ
        message.ack()
        #1. Retrieve the callback result.
        try:
            result = self.callback(*result['args'], **result['kwargs'])
        except:#pylint:disable=bare-except
            result = {'__except__': traceback.format_exc()}
            publish(result,
                    routing_key=message.properties['reply_to'],
                    correlation_id=message.properties['correlation_id'],
                   )
            return
        #2. Convert the callback result to a generator
        if not isinstance(result, types.GeneratorType):
            result = iter((result,))
        #3. Now iterate over the result until the end.
        # If there is an exception, stop iterating.
        try:
            for res in result:
                publish(res,
                        routing_key=message.properties['reply_to'],
                        correlation_id=message.properties['correlation_id'],
                       )
        except:#pylint:disable=bare-except
            res = {'__except__': traceback.format_exc()}
            publish(res,
                    routing_key=message.properties['reply_to'],
                    correlation_id=message.properties['correlation_id'],
                   )
