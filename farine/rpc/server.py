#-*- coding:utf-8 -*-
"""
RPC over AMQP implementation: server side.
"""
from kombu import Connection, Producer, Queue

import farine.amqp

class Server(farine.amqp.Consumer):
    """
    RPC Server which is
    an AMQP consumer then producer.
    """
    prefetch_count = 1
    routing_key_format = '{service}__{callback_name}'

    @farine.amqp.publish()
    def main_callback(self, publish, result, message):
        message.ack()
        try:
            result = self.callback(*result['args'], **result['kwargs'])
        except Exception as e:
            result = {'__except__': str(e)}
        publish(result,
                routing_key=message.properties['reply_to'],
                correlation_id=message.properties['correlation_id'],
        )
