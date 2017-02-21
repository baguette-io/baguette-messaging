#-*- coding:utf-8 -*-
import json
from fixtures import *
import farine.rpc as rpc

def test_rpc_call(rpc_server_factory, rpc_client_factory, rabbitmq_proc, rabbitmq):
    """
    Test that when a client call the RPC server,
    its message is processed.
    """
    server = rpc_server_factory()
    client = rpc_client_factory()
    worker_server = rpc.Server(service='server', callback=server.rpc_method)
    worker_server.start(forever=False)
    client.call()
