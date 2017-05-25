#-*- coding:utf-8 -*-
import json
from fixtures import *
import farine.stream as stream

def test_sse_call_ok(sse_server_factory, sse_client_factory):
    """
    Test that when a client call the stream
    an event is received.
    """
    client = sse_client_factory()

def test_sse_call_timeout(sse_server_factory, sse_client_factory):
    """
    Test that when a client call a non returning event HTTP SSE server,
    it timeouts.
    """
    client = sse_client_factory()

def test_sse_call_exception(sse_server_factory, sse_client_factory):
    """
    Test that when the server raises an error, it's propagated
    to the client.
    """
    client = sse_client_factory()

