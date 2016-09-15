#-*- coding:utf-8 -*-
"""
Entrypoint of the package.
Can start a module here.
"""
import argparse
import kombu.log
import farine.discovery
import farine.settings
import farine.log

farine.log.setup_logging(__name__)
kombu.log.setup_logging()

def main(service=None):
    """
    Entry point.
    """
    if not service:
        #Parsing
        parser = argparse.ArgumentParser()
        parser.add_argument('-s', '--start', type=str, help='Start the service',
                            dest='service', required=True)
        parser.add_argument('-m', '--module', type=str, help='Start the module',
                            dest='module')
        args = parser.parse_args()
        if not args.service and not args.module:
            parser.error('Please specify --start or --module')
        service = args.service
        module = args.module
    #1. Load settings
    farine.settings.load()
    #2. Load the module
    farine.discovery.import_module(service, module)
    #3. Start the module
    farine.discovery.start()
