#-*- coding:utf-8 -*-
import os

def pytest_configure(config):
    os.environ['FARINE_INI'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'farine.ini')
