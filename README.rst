==================
baguette-messaging
==================

Tiny Framework to build micro services.
Currently only support **amqp** based micro service.


How it works
============


AMQP
----

.. code:: python

	import farine.amqp
	
	class Publish(object):
	
	    @farine.amqp.publish(exchange='consume', routing_key='routing_key')
	    def publish_dummy(self, publish):
	        self.publish({'result':0})
	
	class Consume(object):
	
	    @farine.amqp.consume(exchange='publish', routing_key='routing_key')
	    def consume_dummy(self, body, message):
	        self.publish_dummy(body)
	        message.ack()
	
	    @farine.amqp.publish(exchange='publish', routing_key='routing_key2')
	    def publish_consumer(self, publish, body):
	        self.publish(body)
 

In this code we declare one service:

* consume : Read messages
* publish : is not a service, as it doesn't have an event loop.


RPC
---


.. code:: python

	import farine.rpc
	
	class Server(object):
	
	    @farine.rpc.method()
	    def call_dummy(self, *args, **kwargs):
	        return True
	
	class Client(object):
	
	    @farine.rpc.client('server')
	    def dummy(self, rpc)
	        return rpc.call_dummy()

In this code we declare two services:

* server : Wait for a call(consumer), and answer(publisher).
* client : Send a call(publisher), and wait for an anwser(consumer).


Configuration
=============

By default the configuration file is located in */etc/farine.ini*.
You can override this path using the environment variable **FARINE_INI**.

It must contains a **DEFAULT** section, then one by service(using the **lowercase class name**)

Example
```````

::

        [DEFAULT]
        amqp_uri = amqp://baguette:baguette@127.0.0.1:5672/baguette

        [consume]
        enabled = true



Launch
======

To launch a service, just run:

.. code:: shell

	farine --start=mymodule


It will try to import *mymodule.service* and launch it.

Debug
=====

If you want to debug,
just add to the message the key **__debug__** set to **True**.
| The micro service will then launch **cProfile**  when receiving this message, and send the result to the **debug** queue
of the message's exchange.
