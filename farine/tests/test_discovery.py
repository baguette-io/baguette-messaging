#-*- coding:utf-8 -*-
import mock
import farine.discovery
from fixtures import *
from farine.amqp import Consumer

def test_import_services_error():
    with pytest.raises(SystemExit):
        farine.discovery.import_module('nonexistentmodule')

def test_import_services_ok():
    assert farine.discovery.import_module('farine.tests.testfarine') == None

def test_start(channel, consumer_factory):
    consumer = consumer_factory()
    assert farine.discovery.ENTRYPOINTS
    assert farine.discovery.start()
