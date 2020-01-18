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
    description='An async ODM for MongoDB and Postgres.',
    install_requires=[
        'inflection==0.3.1',
        'motor==2.0.0',
        'fire_asynctest==0.0.1'
    ],
    dependency_links=[
        'git+https://github.com/sugarush/fire-asynctest@master#egg=fire_asynctest-0.0.1'

    ]
)
