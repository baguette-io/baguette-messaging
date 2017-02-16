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

    @farine.amqp.publish()
    def call(self, message, publish):
        publish(result,
                routing_key=message.properties['reply_to'],
                correlation_id=uuid.uuid4().hex
        )
        self.start(False)

    def main_callback(self, body, message, publish):
        result = {}
        message.ack()
