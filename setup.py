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
              'mock==2.0.0',
              'pytest==2.9.2',
              'pytest-dbfixtures==0.14.3',
              'pytest-cov==2.3.0',
              'pylint==1.6.1',
              'rabbitpy==0.26.2',
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
          'farine.tests':['rabbit.ini'],
          'farine.logging':['logging.yaml'],
      },
     )
