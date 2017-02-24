#-*- coding:utf-8 -*-
import json
import socket
from fixtures import *
import farine.rpc as rpc

def test_rpc_call(rpc_server_factory, rpc_client_factory, rabbitmq_proc, rabbitmq):
    """
    Test that when a client call the RPC server,
    its message is processed.
    """
    server = rpc_server_factory()
    client = rpc_client_factory()
    assert client.call() == True

def test_rpc_call_timeout(rpc_client_factory, rabbitmq_proc, rabbitmq):
    """
    Test that when a client call a non existing RPC server,
    it timeouts.
    """
    client = rpc_client_factory()
    with pytest.raises(socket.timeout):
        client.call()
