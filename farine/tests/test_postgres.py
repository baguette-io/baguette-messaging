#-*-coding:utf-8 -*-
import farine.connectors.sql.entrypoints
from pytest_postgresql import factories
from fixtures import *

postgresql_proc = factories.postgresql_proc()
postgres = factories.postgresql('postgresql_proc')

def test_postgres_simple(postgres, rpc_server_factory, rpc_client_factory, rabbitmq_proc, rabbitmq):
    """
    Try to create an object and then count them : must succeed.
    """
    clear_rabbitmq(rabbitmq_proc, rabbitmq)
    db = farine.connectors.sql.setup(farine.settings.server)
    db.execute_sql('CREATE TABLE "user" ("id" SERIAL NOT NULL PRIMARY KEY, "name" VARCHAR(255) NOT NULL)')
    db.close()
    server1 = rpc_server_factory('save')
    server2 = rpc_server_factory('get')
    client = rpc_client_factory()
    #
    assert client.save('david') == True
    assert client.get() == 1
    #
    db.connect()
    assert db.execute_sql('SELECT name FROM "user"').fetchall() == [('david',)]
    db.close()
