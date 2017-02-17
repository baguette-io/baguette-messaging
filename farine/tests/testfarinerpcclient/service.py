#-*-coding:utf-8 -*-
import farine.rpc as rpc

class RPCClient(object):
    """
    """

    @rpc.client(exchange="RPCServer")
    def test_client(self, client):
        """
        """
        return client.method()


RPCClient().test_client()
