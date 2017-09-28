#-*- coding:utf-8 -*-
import farine.discovery
from peewee import *

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
