#-*- coding:utf-8 -*-
import json
from fixtures import *
from farine.rpc import Server

def test_rpc_call(rpc_server_factory, rabbitmq_proc, rabbitmq):
    """
    Test that when a client call the RPC server,
    its message is processed.
    """
    server = rpc_server_factory()
    worker_server = Server(service='rpcserver', callback=server.method)
