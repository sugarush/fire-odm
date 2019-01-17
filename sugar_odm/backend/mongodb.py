import inflection
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ReturnDocument

from .. util import serialize
from .. model import Model, Field, Error


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
    def initialize(cls):
        if cls.__name__ == 'MongoDBModel':
            return

        if not hasattr(cls, 'connection_options'):
            cls.connection_options = { }

        if not hasattr(cls, 'database_options'):
            cls.database_options = { 'name': 'test' }

        if not hasattr(cls, 'collection_options'):
            cls.collection_options = { 'name': cls._table }

        cls.connection = MongoDB.connect(**cls.connection_options)
        cls.database = cls.connection.get_database(**cls.database_options)
        cls.collection = cls.database.get_collection(**cls.collection_options)

    @classmethod
    def default_primary(cls):
        field = Field()
        field.name = '_id'
        field.primary = True
        field.type = str
        return field

    @classmethod
    def check_primary(cls, primary):
        if not primary.name is '_id':
            raise AttributeError('MongoDBModel primary key name must be: _id')

        if not primary.type is str:
            raise AttributeError('MongoDBModel primary key type must be: ObjectId')

    @classmethod
    async def drop(cls):
        await cls.collection.drop()

    @classmethod
    async def exists(cls, id):
        if id:
            document = await cls.collection.find_one(
                { '_id': ObjectId(id) },
                { '_id': True }
            )
            if document:
                return True
            return False
        else:
            raise Error(
                title = 'Document Exists Failed',
                detail = 'No document ID provided.'
            )

    @classmethod
    async def find_one(cls, id):
        if id:
            document = await cls.collection.find_one(
                { '_id': ObjectId(id) }
            )
            if document:
                return cls(document)
            else:
                raise Error(
                    title = 'Document Find One Failed',
                    detail = 'No document returned.'
                )
        else:
            raise Error(
                title = 'Document Find One Failed',
                detail = 'No document ID provided.'
            )

    @classmethod
    async def find(cls, *args, **kargs):
        cursor = cls.collection.find(*args, **kargs)
        async for document in cursor:
            yield cls(document)

    @classmethod
    async def add(cls, args):
        if isinstance(args, dict):
            model = cls(args)
            await model.save()
            return model
        elif isinstance(args, list):
            models = [ ]
            for data in args:
                model = cls(data)
                await model.save()
                models.append(model)
            return models
        else:
            raise Error(
                title = 'Document Add Failed',
                detail = 'Invalid argument to MongoDBModel.add: must be a list or dict.'
            )

    async def save(self):
        self.validate()

        if self.id:
            data = self.serialize(computed=True, controllers=True, reset=True)
            del data['_id']
            document = await self.collection.find_one_and_update(
                { '_id': ObjectId(self.id) },
                { '$set': data },
                return_document=ReturnDocument.AFTER
            )
            if document:
                self.update(document)
            else:
                raise Error(
                    title = 'Document Save Failed',
                    detail = 'No document returned.'
                )
        else:
            data = self.serialize(computed=True, controllers=True, reset=True)
            result = await self.collection.insert_one(data)
            if result:
                self.id = result.inserted_id
                await self.load()
            else:
                raise Error(
                    title = 'Document Save Failed',
                    detail = 'Inserted ID not available or non-existent.'
                )

    async def load(self):
        if self.id:
            document = await self.collection \
                .find_one({ '_id': ObjectId(self.id) })
            if document:
                self.update(document)
            else:
                raise Error(
                    title = 'Document Load Failed',
                    detail = 'No document returned.'
                )
        else:
            raise Error(
                title = 'Document Load Failed',
                detail = 'No document ID, cannot load.'
            )

    async def delete(self):
        if self.id:
            result = await self.collection \
                .delete_one({ '_id': ObjectId(self.id) })
            if result:
                if result.deleted_count == 0:
                    raise Error(
                        title = 'Document Delete Failed',
                        detail = 'Deleted count is zero.'
                    )
                else:
                    self._data = { }
            else:
                raise Error(
                    title = 'Document Delete Failed',
                    detail = 'Collection operation result is a falsy value.'
                )
        else:
            raise Error(
                title = 'Document Delete Failed',
                detail = 'No document ID, cannot delete.'
            )
