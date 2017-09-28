#-*-coding:utf-8 -*-
from pytest_postgresql import factories
from fixtures import *

postgresql_proc = factories.postgresql_proc()
postgres = factories.postgresql('postgresql_proc')

def test_postgres_simple(postgres,rpc_server_factory, rpc_client_factory, rabbitmq_proc, rabbitmq):
    """
    Try to import and create an object.
    """
    clear_rabbitmq(rabbitmq_proc, rabbitmq)
    server = rpc_server_factory('save')
    client = rpc_client_factory()
    assert client.save('david') == True
