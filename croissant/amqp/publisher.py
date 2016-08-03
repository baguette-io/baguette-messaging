#-*- coding:utf-8 -*-
"""
The publisher module manage all the producer's messages workflow:
    - Connection to the server
    - Publish the message to an exchange
    - Error handler (reconnection, retry, etc.)
"""
import logging
from kombu import Connection, Exchange
from kombu.pools import producers, connections
import croissant.settings

LOGGER = logging.getLogger(__name__)

class Publisher(object):
    """
    Publisher generic class. Also known as Producer.
    """

    def __init__(self, service, routing_key):
        """
        Messages will be published to `exchange`, using these different settings.
        :param service: The publisher's service. Will also served as exchange, required.
        :type service: str
        :param routing_key: The key used to route the message.
        :type routing_key: None, str
        :rtype: None
        """
        self.settings = getattr(croissant.settings, service)
        self.routing_key = routing_key
        self.exchange = Exchange(service, type=self.settings['type'],
                                 durable=self.settings['durable'],
                                 auto_delete=self.settings['auto_delete'],
                                 delivery_mode=self.settings['delivery_mode'])
    def get_connection(self):
        """
        Retrieve the connection, lazily.

        :returns: The broker connection.
        :rtype: kombu.connection.Connection
        """
        return Connection(self.settings['amqp_uri'])

    def send(self, message):
        """
        Send the the `message` to the broker.

        :param message: The message to send. Its type depends on the serializer used.
        :type message: object
        :rtype: None
        """
        conn = self.get_connection()
        with connections[conn].acquire(block=True) as connection:
            self.exchange.maybe_bind(connection)
            with producers[connection].acquire(block=True) as producer:
                LOGGER.info('Send message %s to exchange %s with routing_key %s',
                            message, self.exchange.name, self.routing_key)
                producer.publish(
                    message,
                    exchange=self.exchange,
                    declare=[self.exchange],
                    serializer=self.settings['serializer'],
                    routing_key=self.routing_key,
                    retry=self.settings['retry'],
                    delivery_mode=self.settings['delivery_mode'],
                    retry_policy=self.settings['retry_policy'])

    def __call__(self, *args, **kwargs):
        return self.send(*args, **kwargs)

    def close(self):
        """
        Release the connection to the broker.

        :rtype: None
        """
        self.get_connection().release()
