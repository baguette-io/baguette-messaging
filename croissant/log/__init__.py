#-*- coding:utf-8 -*-
"""
Module which setup the logging using a yaml file.
"""
import logging
import logging.config
import os
import yaml

def setup_logging(app, disable_existing_loggers=True):
    """
    Setup the logging using logging.yaml.
    :param app: The app which setups the logging. Used for the log's filename and for the log's name.
    :type app: str
    :param disable_existing_loggers: If False, loggers which exist when this call is made are left enabled.
    :type disable_existing_loggers: bool
    :returns: None
    """
    conf = yaml.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logging.yaml'), 'r'))
    conf['disable_existing_loggers'] = disable_existing_loggers
    conf['loggers'][app] = conf['loggers'].pop('__name__')
    logging.config.dictConfig(conf)
