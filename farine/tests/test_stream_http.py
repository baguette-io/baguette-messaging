#-*- coding:utf-8 -*-
import json
from fixtures import *
import farine.rpc as rpc

def test_stream_http_call_ok(http_stream_server_factory, http_stream_client_factory):
    """
    Test that when a client call the streamm
    an event is received.
    """
    client = http_stream_client_factory()

def test_stream_http_call_timeout(http_stream_server_factory, http_stream_client_factory):
    """
    Test that when a client call a non returning event http server,
    it timeouts.
    """
    client = http_stream_client_factory()

def test_stream_http_call_exception(http_stream_server_factory, http_stream_client_factory):
    """
    Test that when the server raises an error, it's propagated
    to the client.
    """
    client = http_stream_client_factory()

