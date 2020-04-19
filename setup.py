__author__ = 'Paul Severance'

from setuptools import setup

setup(
    name='sugar-odm',
    version='0.0.1',
    author='Paul Severance',
    author_email='paul.severance@gmail.com',
    url='https://github.com/sugarush/sugar-odm',
    packages=[
        'sugar_odm',
        'sugar_odm.backend',
        'sugar_odm.controller'
    ],
    description='An asynchronous ODM for MongoDB, Postgres and RethinkDB.',
    install_requires=[
        'sugar-asynctest@git+https://github.com/sugarush/sugar-asynctest@master',
        'inflection',
        'motor',
        'asyncpg',
        'ipython',
        'rethinkdb'
    ]
)
