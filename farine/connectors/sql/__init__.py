#-*- coding:utf-8 -*-
import json
import farine.discovery
import sel.serializers
from peewee import Model as PModel
from peewee import *
from playhouse.shortcuts import model_to_dict
try:
    from playhouse.postgres_ext import *
except ImportError:
    pass


class Model(PModel):
    """
    Base model that extends the peewee one.
    """

    def to_json(self):
        """
        Convert a model into a json using the playhouse shortcut.
        """
        return json.dumps(model_to_dict(self), cls=sel.serializers.JsonEncoder)

class Meta:
    database = None

def setup(settings):
    """
    Setup the database connection.
    """
    connector = settings.get('db_connector')
    if connector == 'postgres':
        from playhouse.pool import PooledPostgresqlExtDatabase
        return PooledPostgresqlExtDatabase(settings['db_name'],
                           user=settings['db_user'],
                           password=settings['db_password'],
                           host=settings['db_host'],
                           port=settings.get('db_port'),
                           max_connections=settings.get('db_max_conn'),
                           stale_timeout=settings.get('db_stale_timeout'),
                           timeout=settings.get('db_timeout'),
                           register_hstore=False)

def init(module, db):
    """
    Initialize the models.
    """
    for model in farine.discovery.import_models(module):
        model._meta.database = db
