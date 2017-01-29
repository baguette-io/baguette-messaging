#-*- coding:utf-8 -*-
"""
Setup for the baguette messaging.
"""
from setuptools import find_packages, setup


setup(name='baguette-messaging',
      version='0.1',
      description='Baguette messaging framework',
      url='baguette.io',
      author_email='dev@baguette.io',
      packages=find_packages(),
      install_requires=[
          'kombu==3.0.35',
          'gevent==1.1.1',
          'PyYAML==3.11',
      ],
      extras_require={
          'testing': [
              'mock',
              'pytest',
              'pytest-rabbitmq',
              'pytest-cov',
              'pylint',
              'rabbitpy',
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
          'farine.tests':['farine.ini', 'rabbit.ini'],
          'farine.log':['logging.yaml'],
      },
     )
