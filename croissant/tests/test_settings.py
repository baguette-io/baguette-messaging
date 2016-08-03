#-*- coding:utf-8 -*-
from fixtures import *
import croissant.settings


def test_defaults():
    assert hasattr(croissant.settings, 'publish')
    assert croissant.settings.publish.has_key('amqp_uri')
    ##
    assert croissant.settings.publish['type'] == 'direct'
    assert croissant.settings.publish['durable'] == True
    assert croissant.settings.publish['auto_delete'] == False
    assert croissant.settings.publish['delivery_mode'] == 2
    assert croissant.settings.publish['retry'] == True
    assert croissant.settings.publish['retry_policy'] == {'max_retries': 5}
    assert croissant.settings.publish['serializer'] == 'json'
