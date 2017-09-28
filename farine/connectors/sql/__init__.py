#-*- coding:utf-8 -*-
import farine.discovery
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
    models = farine.discovery.import_models(module)
    for model in models:
        model = type(model.__name__, (BaseModel,), dict(model.__dict__))
        #model.__bases__ = (BaseModel, object,)
        model.create_table(fail_silently=True)
    db.close()
