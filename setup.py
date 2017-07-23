#-*- coding:utf-8 -*-
'''
Setup for the baguette messaging.
'''
from setuptools import find_packages, setup


setup(name='baguette-messaging',
      version='0.1',
      description='Baguette messaging framework',
      long_description=open('README.rst').read(),
      url='https://github.com/baguette-io/baguette-messaging/',
      author_email='pydavid@baguette.io',
      keywords=['micro', 'services', 'amqp', 'rpc', 'messaging'],
      classifiers=[
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.7',
          'License :: OSI Approved',
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
          'Operating System :: OS Independent',
          'Topic :: Software Development :: Libraries :: Application Frameworks',
      ],
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
