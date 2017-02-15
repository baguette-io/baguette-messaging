#-*- coding:utf-8 -*-
"""
RPC over AMQP implementation: server side.
"""

from kombu import Connection, Producer, Queue

import farine.amqp

class Server(farine.amqp.Consumer):
    """
    RPC Server which is
    an AMQP consumer.
    """
    prefetch_count = 1

    @farine.amqp.publish()
    def main_callback(self, body, message, publish):
        result = {}
        publish(result,
                exchange="",
                routing_key=message.properties['reply_to'],
                correlation_id=message.properties['correlation_id'],
        )
        message.ack()
