__author__ = 'Lucifer Avada'

from setuptools import setup

setup(
    name='sugar-odm',
    version='0.0.1',
    author='Lucifer Avada',
    author_email='lucifer.avada@gmail.com',
    url='https://github.com/sugarush/sugar-odm',
    packages=['sugar_odm'],
    description='An async ODM for MongoDB.',
    install_requires=[
        'sugar_asynctest==0.0.1'
    ],
    dependency_links=[
        'git+https://github.com/sugarush/sugar-asynctest@f652ade886214ecb74beeb39f6fb5533e03305ed#egg=sugar_asynctest-0.0.1'

    ]
)
