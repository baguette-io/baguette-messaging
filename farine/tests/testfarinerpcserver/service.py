#-*-coding:utf-8 -*-
import farine.rpc as rpc

class RPCServer(object):
    """
    """

    @rpc.method()
    def method(self, *args, **kwargs):
        """
        """
        print args
        print kwargs
        return "ok"
