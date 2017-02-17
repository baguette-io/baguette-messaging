#-*- coding:utf-8 -*-
"""
Module containing the configuration.

To load the configuration, call the `load()` function.

By default the configuration's filepath */etc/farine.ini* will be use.
To override it, set the environment variable **FARINE_INI**.

The format of the config must be compliant with configparser,
have a [DEFAULT] section and one by service.


Example:

| [DEFAULT]
| amqp_uri=amqp://user:password@localhost:5672/vhost

| [taskstatus]
| enabled = true
"""
import os
import ConfigParser

CONF_PATH = os.environ.get('FARINE_INI', '/etc/farine.ini')
DEFAULTS = {
    'type': 'direct', #Exchange's type : `direct`, `topic`, `broadcast`
    'durable': True, #Does the exchange still exist after the AMQP server restart.
    'auto_declare': True, #Does the queue auto declare itself.
    'delivery_mode': 2, #How the messages are stored in the server. Transient=>1 or Persistent=>2
    'retry': True, #Retry sending message or declaring the exchange if the connection is lost.
    'retry_policy' : {'max_retries': 5}, #Retry's policy.
    'serializer': 'json', #The serializer used to encode the message.
}

def load():
    """
    | Load the configuration file.
    | Add dynamically configuration to the module.

    :rtype: None
    """
    config = ConfigParser.RawConfigParser(DEFAULTS)
    config.readfp(open(CONF_PATH))
    for section in config.sections():
        globals()[section] = {}
        for key, val in config.items(section):
            globals()[section][key] = val
