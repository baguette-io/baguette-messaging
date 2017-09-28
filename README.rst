==================
baguette-messaging
==================

.. image:: https://travis-ci.org/baguette-io/baguette-messaging.svg?branch=master
    :target: https://travis-ci.org/baguette-io/baguette-messaging

Tiny Framework to build micro services.
Currently only support **amqp**, **rpc over amqp** and **http stream** based micro services.

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


Database
========

| *baguette-messaging* is using peewee to manage databases connections (only postgresql is supported for the moment)
| In order for it to detect that you are using a database, you need to create a **models.py** module.
| Then, each time we enter into a method (amqp,rpc,stream) a database connection will be created and closed.
| You can use the database connection using **self.db**, to manage transactions for example.

Example
-------

models.py:

.. code:: python

    from farine.connectors.sql import *
    
    class User(object):
        name = CharField()

service.py:

.. code:: python

	import farine.amqp
	from models import User
	
	class Client(object):

	    @farine.amqp.consume(exchange='exchange', routing_key='routing_key')
	    def select(self, body, message):
	        return User.select().where(User.id==1)


Overview
========

| You can mix in a service, everything:
| it can be a consumer of an HTTP stream, and send back the result in RPC, etc.

Example
--------

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


Database
--------

If you use a database connection, you have to add in the **[DEFAULT]** section the db parameters:

::

    [DEFAULT]
    db_connector = postgres (required)
    db_name = name (required)
    db_user = user (required)
    db_host = host (required)
    db_password = password (required)
    db_port = port (optional)
    db_max_conn = max_connections (optional)
    db_stale_timeout = stale timeout (optional)
    db_timeout = timeout (optional)


Launch
======

To launch a service, just run:

.. code:: shell

	farine --start=mymodule

It will try to import *mymodule.service* and launch it.
