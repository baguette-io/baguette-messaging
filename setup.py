#-*- coding:utf-8 -*-
"""
Setup for the baguette messaging.
"""
from setuptools import find_packages, setup


setup(name='baguette-messaging',
      version='0.1',
      description='Baguette messaging framework',
      url='baguette.io',
      author='https://github.com/baguette-io/baguette-messaging/',
      author_email='pydavid@baguette.io',
      keywords=['micro','services','amqp','rpc'],
      packages=find_packages(),
      install_requires=[
          'baguette-utils',
          'gevent==1.1.1',
          'kombu==4.0.2',
          'PyYAML==3.11',
          'sseclient==0.0.18',
      ],
      extras_require={
          'testing': [
              'mock',
              'pytest',
              'pytest-rabbitmq',
              'pytest-cov',
              'pylint',
              'rabbitpy',
              'requests-mock',
          ],
          'doc': [
              'Sphinx==1.4.4',
          ],
      },
      entry_points={
          'console_scripts':[
              'farine=farine.main:main',
          ],
      },
      package_data={
          'farine.tests':['farine.ini', 'pytest.ini'],
          'farine.log':['logging.yaml'],
      },
     )
