#-*- coding:utf-8 -*-
import json
from fixtures import *

def test_execute_method(execute_client_factory):
    """
    Test that when a client call the stream
    """
    client = execute_client_factory()
    worker_client = execute.Method(service='executemethodclient', callback=client.mymethod)
    assert worker_client.start(restart=False) == 'executed'
