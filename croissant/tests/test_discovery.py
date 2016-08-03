#-*- coding:utf-8 -*-
import mock
import croissant.discovery
from fixtures import *
from croissant.amqp import Consumer

def test_import_services_error():
    with pytest.raises(SystemExit):
        croissant.discovery.import_module('nonexistentmodule')

def test_import_services_ok():
    assert croissant.discovery.import_module('test_discovery') == None

def test_start(channel, consumer_factory):
    consumer = consumer_factory()
    assert croissant.discovery.ENTRYPOINTS
    assert croissant.discovery.start()
