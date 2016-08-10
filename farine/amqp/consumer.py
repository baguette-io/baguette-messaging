#-*- coding:utf-8 -*-
"""
The consumer module manage all the consumer's messages workflow:
    - Connection to the server
    - Consume the message from an exchange
    - Error handler (reconnection, retry, etc.)
"""
import contextlib
import cProfile
import pstats
import StringIO
from kombu import Connection, Exchange, Queue
from kombu.pools import producers
from kombu.mixins import ConsumerMixin
from farine.mixins import EntryPointMixin
import farine.settings

class Consumer(ConsumerMixin, EntryPointMixin):
    """
    Consumer generic class.
    """

    def __init__(self, *args, **kwargs):#pylint:disable=unused-argument
        """
        :param service: The service's name which consume.
        :type service: str
        :param queue_name: The name of queue. Optional, default to `service` value.
        :type queue_name: None, str
        :param exhange: The exchange's name to consume from.
        :type exchange: str
        :param exchange_type: The exchange's type. Default to 'direct'.
        :type exchange_type: str
        :param routing_key: The routing key to read the message.
        :type routing_key: str
        :param callback: The callback to call when receiving a message.
        :type callback: object
        :rtype: None
        """
        self.service = kwargs.pop('service')
        self.settings = getattr(farine.settings, self.service)
        self.callback = kwargs.pop('callback')
        exchange_type = kwargs.pop('exchange_type', 'direct')
        self.exchange = Exchange(kwargs.pop('exchange'),
                                 type=exchange_type,
                                 durable=self.settings['durable'],
                                 auto_declare=self.settings['auto_declare'],
                                 delivery_mode=self.settings['delivery_mode'])
        self.queue = Queue(kwargs.get('queue_name', self.service),
                           exchange=self.exchange,
                           routing_key=kwargs['routing_key'],
                           durable=self.settings['durable'],
                           auto_declare=self.settings['auto_declare'])
        self.connection = Connection(self.settings['amqp_uri'])

    def get_consumers(self, _Consumer, channel):
        """
        | ConsumerMixin requirement.
        | Get the consumers list.

        :returns: All the consumers.
        :rtype: list.
        """
        return [_Consumer(queues=[self.queue], callbacks=[self.main_callback])]


    @contextlib.contextmanager
    def debug(self, body, message):#pylint:disable=arguments-differ,unused-argument
        """
        | Rewrite/move some code?
        | EntryPointMixin requirement. Context Manager.
        | Check if debug is enabled for the message consumed.
        | If so will run cProfile for this message, and send the result
        | to the `__debug__` queue of the exchange.

        :param callback: the callback of the message consumed.
        :type callback: function
        :rtype: None
        """
        is_debug = body.get('__debug__', False)
        if not is_debug:
            yield
        else:
            #Start the profiler
            result = StringIO.StringIO()
            profiler = cProfile.Profile()
            profiler.enable()
            yield
            #Close the profiler
            profiler.disable()
            profiler.create_stats()
            stats = pstats.Stats(profiler, stream=result)
            stats.strip_dirs().print_stats()
            debug_message = body.copy()
            debug_message['__debug__'] = result.getvalue()
            #Send the result to the exchange
            with producers[self.connection].acquire(block=True) as producer:
                debug_queue = Queue('debug',
                                    exchange=self.exchange,
                                    routing_key='debug',
                                    durable=True,
                                    auto_declare=True)
                producer.maybe_declare(debug_queue)
                producer.publish(debug_message,
                                 exchange=self.exchange,
                                 declare=[self.exchange],
                                 routing_key='debug')


    def start(self, *args, **kwargs):#pylint:disable=unused-argument
        """
        | Launch the consumer.
        | It can listen forever for messages or just wait for one.

        :param forever: If set, the consumer listens forever. Default to `True`.
        :type forever: bool
        :rtype: None
        """
        forever = kwargs.get('forever', True)
        if forever:
            return self.run()
        next((self.consume(limit=1)), None)

    def stop(self):
        """
        Stop to consume.

        :rtype: None
        """
        self.should_stop = True
        self.connection.release()
