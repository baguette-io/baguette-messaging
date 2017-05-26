#-*- coding:utf-8 -*-
import json
from fixtures import *

def test_sse_call_ok(sse_server_ok, sse_client_factory):
    """
    Test that when a client call the stream
    an event is received.
    """
    client = sse_client_factory()
    worker_client = stream.SSEConsumer(service='streamsseclient', callback=client.event)
    assert client.messages_consumed == 0
    worker_client.start(limit=1)
    assert client.messages_consumed == 1
