#-*- coding:utf-8 -*-
"""
Entrypoint of the package.
Can start a module here.
"""
import argparse
import kombu.log
import croissant.discovery
import croissant.settings
import croissant.log

croissant.log.setup_logging(__name__)
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
    croissant.settings.load()
    #2. Load the module
    croissant.discovery.import_module(args.service)
    #3. Start the module
    croissant.discovery.start()
