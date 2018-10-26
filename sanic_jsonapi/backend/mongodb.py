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
