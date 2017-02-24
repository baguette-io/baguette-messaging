#-*- coding:utf-8 -*-
from fixtures import *
import farine.settings


def test_defaults():
    assert hasattr(farine.settings, 'publish')
    assert farine.settings.publish.has_key('amqp_uri')
    ##
    assert farine.settings.publish['type'] == 'direct'
    assert farine.settings.publish['durable'] == True
    assert farine.settings.publish['delivery_mode'] == 2
    assert farine.settings.publish['retry'] == True
    assert farine.settings.publish['retry_policy'] == {'max_retries': 5}
    assert farine.settings.publish['serializer'] == 'json'
