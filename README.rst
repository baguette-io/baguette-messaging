==================
baguette-messaging
==================

Tiny Framework to build micro services.
Currently only support **amqp**, **rpc over amqp** and **http stream** based micro services.

.. image:: https://travis-ci.org/baguette-io/baguette-messaging.svg?branch=master
    :target: https://travis-ci.org/baguette-io/baguette-messaging


How it works
============


AMQP
----

| We declare a publisher:
| the method decorated takes one parameter **publish** (farine.amqp.publisher.Publisher)

.. code:: python

	import farine.amqp
	
	class Publish(object):
	
	    @farine.amqp.publish(exchange='consume', routing_key='routing_key')
	    def publish_dummy(self, publish):
                """
                :param publish: Send the data through AMQP.
                :type publish: farine.amqp.publisher.Publisher
	        """
	        publish({'result':0})
	
| And then a consumer :
| the method decorated takes two parameters **body** (dict) and **message** (kombu.message.Message).

.. code:: python

	import farine.amqp

	class Consume(object):
	
	    @farine.amqp.consume(exchange='publish', routing_key='routing_key')
	    def consume_dummy(self, body, message):
                """
                :param body: The message's data.
                :type body: dict
                :param message: Message class.
                :type message: kombu.message.Message
                """
	        message.ack()
 


RPC over AMQP
-------------

| We need declare two services :
| the server : Wait for a call(consumer), and answer(publisher).
| The method decorated just takes **args** and **kwargs**

.. code:: python

	import farine.rpc
	
	class Server(object):
	
	    @farine.rpc.method()
	    def dummy(self, *args, **kwargs):
	        return True
	

| And the client : Send a call(publisher), and wait for an answer(consumer).
| the method decorated takes one argument **rpc** (farine.rpc.client.Client).
| The result will be a dictionnary.

.. code:: python

	import farine.rpc
	
	class Client(object):
	
            @farine.rpc.client('myotherservice')
	    def dummy(self, rpc):
                """
                :param rpc: The RPC client.
                :type rpc: farine.rpc.client.Client
                """
	        result = rpc.dummy()


RPC Stream
----------

| We can also do streaming RPC call.
| All you need to do is to add *__stream__ = True** to your RPC call.
| Also, a generator is returned.

Example:

.. code:: python

	import farine.rpc
	
	class Server(object):
	
	    @farine.rpc.method()
	    def dummy(self, *args, **kwargs):
	        yield 'a'
	        yield 'b'
	
.. code:: python

	import farine.rpc
	
	class Client(object):
	
	    @farine.rpc.client('myotherservice')
	        def dummy(self, rpc):
                """
                :param rpc: The RPC client.
                :type rpc: farine.rpc.client.Client
                """
	        for result in rpc.dummy(__stream__=True):
                    print result


HTTP Stream
-----------

| We can declare a service that will listen to an HTTP SSE event :
| the method decorated takes one argument **data** (dict).

.. code:: python

	import farine.stream
	
	class Client(object):
	
	    @farine.stream.http()
	    def listen_event(self, data):
                """
                :param data: The event sent.
                :type data: dict
                """
	        return True

Overview
--------

| You can mix in a service everything:
| it can be a consumer to an HTTP stream, and send back the result in RPC, etc.

Example:

.. code:: python

	import farine.rpc
	import farine.stream
	
	class Client(object):

            @farine.stream.http()
            def get(self, data):
                return self.send(data)

	    @farine.rpc.client('myotherservice')
	    def send(self, rpc, data):
	        return rpc.process(data)


Configuration
=============

By default the configuration file is located in */etc/farine.ini*.
You can override this path using the environment variable **FARINE_INI**.

| It must contains one section by service (using the **lowercase class name**).
| a **DEFAULT** section can also be present.

Example
-------

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
