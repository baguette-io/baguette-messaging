#-*- coding:utf-8 -*-
from peewee import *

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
    meta = type('Meta', (object,), {'database':db})
    BaseModel = type('BaseModel', (Model,), {'Meta': meta})
    models = farine.discovery.import_model(module)
    for model in models:
        print model.__class__
        model.__class__ = type(model.__class__,(BaseModel,), {})
        model.create_table(fail_silently=True)
