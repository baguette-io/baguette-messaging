Tiny Framework to build micro services.
Currently only support **amqp** based micro service.


How it works
============


.. code:: python

	import farine.amqp
	
	class Publish(object):
	
	    @farine.amqp.publish()
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


Publisher
`````````

To declare a publisher, just put the decorator **@farine.amqp.publish** on the top of your method,
then use **publish(message)** inside it to send the message.
It will auto declare and send it to the **lowercase class name** exchange with also **lowercase class name** as routing_key.
If you want to publish to another exchange/with another routing key add the **exchange**/**routing_key** parameter in the decorator.


Consumer
````````

To declare a consumer, just put the decorator **@farine.amqp.consume(exchange='publish', routing_key='routing_key')**
on the top of your method, which must contains two arguments: **body** and **message**.


Configuration
=============


By default the configuration file is located in */etc/farine.ini*.
You can override this path using the environment variable **FARINE_CONF_FILE**.

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


It will inspect the module for services, and launch the 'bootable' ones (the consumers).

Debug
=====

If you want to debug,
just add to the message the key **__debug__** set to **True**.
| The micro service will then launch **cProfile**  when receiving this message, and send the result to the **debug** queue
of the message's exchange.
