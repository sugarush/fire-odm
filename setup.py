__author__ = 'Paul Severance'

from setuptools import setup

setup(
    name='fire-odm',
    version='0.0.1',
    author='Paul Severance',
    author_email='paul.severance@gmail.com',
    url='https://github.com/sugarush/fire-odm',
    packages=[
        'fire_odm',
        'fire_odm.backend',
        'fire_odm.controller'
    ],
    description='An asynchronous ODM for MongoDB and Postgres.',
    install_requires=[
        'fire-asynctest@git+https://github.com/sugarush/fire-asynctest@master',
        'inflection',
        'motor',
        'ujson',
        'asyncpg',
        'ipython'
    ]
)
