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
import farine.settings

LOGGER = logging.getLogger(__name__)

class Publisher(object):
    """
    Publisher generic class. Also known as Producer.
    """
    auto_delete = False

    def __init__(self, name, routing_key, service=None):
        """
        Messages will be published to `exchange`, using these different settings.
        :param name: The exchange name, required.
        :type name: str
        :param routing_key: The key used to route the message.
        :type routing_key: None, str
        :param service: The service's name. Used to get the configuration
        :type service: None, str
        :rtype: None
        """
        self.settings = getattr(farine.settings, service or name)
        self.routing_key = routing_key
        self.exchange = Exchange(name, type=self.settings['type'],
                                 durable=self.settings['durable'],
                                 auto_delete=self.settings.get('auto_delete', self.auto_delete),
                                 delivery_mode=self.settings['delivery_mode'])
    def get_connection(self):
        """
        Retrieve the connection, lazily.

        :returns: The broker connection.
        :rtype: kombu.connection.Connection
        """
        return Connection(self.settings['amqp_uri'])

    def send(self, message, *args, **kwargs):
        """
        Send the the `message` to the broker.

        :param message: The message to send. Its type depends on the serializer used.
        :type message: object
        :rtype: None
        """
        routing_keys = kwargs.get('routing_key') or self.routing_key
        routing_keys = [routing_keys] if isinstance(routing_keys, basestring) else routing_keys
        correlation_id = kwargs.get('correlation_id', None)
        reply_to = kwargs.get('reply_to', None)
        reply_to_name = reply_to.name if reply_to else None
        conn = self.get_connection()
        with connections[conn].acquire(block=True) as connection:
            self.exchange.maybe_bind(connection)
            with producers[connection].acquire(block=True) as producer:
                for routing_key in routing_keys:
                    LOGGER.info('Send message %s to exchange %s with routing_key %s reply_to %s correlation_id %s',
                                message, self.exchange.name, routing_key, reply_to_name, correlation_id)
                    producer.publish(
                        message,
                        exchange=self.exchange,
                        declare=[self.exchange],
                        serializer=self.settings['serializer'],
                        routing_key=routing_key,
                        correlation_id=correlation_id,
                        retry=self.settings['retry'],
                        delivery_mode=self.settings['delivery_mode'],
                        reply_to=reply_to_name,
                        retry_policy=self.settings['retry_policy'])

    def __call__(self, *args, **kwargs):
        return self.send(*args, **kwargs)

    def close(self):
        """
        Release the connection to the broker.

        :rtype: None
        """
        self.get_connection().release()
