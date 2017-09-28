#-*- coding:utf-8 -*-
"""
Entrypoint of the sql connectors.
"""
import argparse
import farine.connectors.sql
import farine.discovery
import farine.settings
import farine.log

farine.log.setup_logging(__name__)

def migrate(module=None):
    """
    Entrypoint to migrate the schema.
    For the moment only create tables.
    """
    if not module:
        #Parsing
        parser = argparse.ArgumentParser()
        parser.add_argument('-s', '--service', type=str, help='Migrate the module', required=True,
                            dest='module')
        args = parser.parse_args()
        module = args.module
    #1. Load settings
    farine.settings.load()
    #2. Load the module
    models = farine.discovery.import_models(module)
    #3. Get the connection
    db = farine.connectors.sql.setup(getattr(farine.settings, module))
    #4. Create tables
    for model in models:
        model._meta.database = db
        model.create_table(fail_silently=True)
