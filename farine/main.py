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

def main():
    """
    Entry point.
    """
    #Parsing
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--start', type=str, help='Start the service',
                        dest='service', required=True)
    args = parser.parse_args()
    #1. Load settings
    farine.settings.load()
    #2. Load the module
    farine.discovery.import_module(args.service)
    #3. Start the module
    farine.discovery.start()
