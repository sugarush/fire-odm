import inflection
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient

from .. util import serialize
from .. model import Model, Field


class MongoDB(object):

    connections = { }

    @classmethod
    def connect(cls, **kargs):
        kargs['connect'] = True
        key = serialize(kargs)

        connection = cls.connections.get(key)
        if connection:
            return connection

        cls.connections[key] = AsyncIOMotorClient(**kargs)
        return cls.connections[key]


class MongoDBModel(Model):

    connection_options = { }
    connection = None

    database_options = { }
    database = None

    collection_options = { }
    collection = None

    @classmethod
    def initialize(cls):
        if cls.__name__ == 'MongoDBModel':
            return

        cls.connection = MongoDB.connect(**cls.connection_options)

        if not cls.database_options.get('name'):
            cls.database_options['name'] = 'test'

        cls.database = cls.connection.get_database(**cls.database_options)

        if not cls.collection_options.get('name'):
            cls.collection_options['name'] = cls._table

        cls.collection = cls.database.get_collection(**cls.collection_options)

    @classmethod
    def default_primary(cls):
        field = Field()
        field.name = '_id'
        field.primary = True
        field.type = ObjectId
        return field

    @classmethod
    def check_primary(cls, primary):
        if not primary.name is '_id':
            raise AttributeError('MongoDBModel primary key name must be: _id')

        if not primary.type is ObjectId:
            raise AttributeError('MongoDBModel primary key type must be: ObjectId')

    @classmethod
    async def exists(cls, id):
        raise NotImplementedError()

    @classmethod
    async def find_one(cls, id):
        raise NotImplementedError()

    @classmethod
    async def find(cls, query={ }):
        raise NotImplementedError()

    @classmethod
    async def add(cls, *args):
        raise NotImplementedError()

    async def save(self):
        raise NotImplementedError()

    async def load(self):
        raise NotImplementedError()

    async def delete(self):
        raise NotImplementedError()
