#-*- coding:utf-8 -*-
import json
import socket
from fixtures import *
import farine.rpc as rpc

def test_rpc_decorator_call(rpc_server_factory, rpc_client_factory, rabbitmq_proc, rabbitmq):
    """
    Test that when a client call the RPC server,
    its message is processed.
    """
    server = rpc_server_factory()
    client = rpc_client_factory()
    assert client.call() == True

def test_rpc_decorator_call_timeout(rpc_client_factory, rabbitmq_proc, rabbitmq):
    """
    Test that when a client call a non existing RPC server,
    it timeouts.
    """
    client = rpc_client_factory()
    with pytest.raises(socket.timeout):
        client.call()

def test_rpc_class_call(rpc_server_factory, rabbitmq_proc, rabbitmq):
    """
    Test that rpc.client.Client() works like rpc.client() decorator:
    its message is processed.
    """
    server = rpc_server_factory()
    client = rpc.Client('server')
    assert client.something() == True

def test_rpc_class_call_timeout(rabbitmq_proc, rabbitmq):
    """
    Test that rpc.client.Client() works like rpc.client() decorator:
    its timeouts.
    """
    client = rpc.Client('server')
    with pytest.raises(socket.timeout):
        client.call()

