import inflection
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ReturnDocument

from .. util import serialize
from .. model import Model, Field


class MongoDB(object):

    connections = { }
    loop = None

    @classmethod
    def connect(cls, **kargs):
        kargs['connect'] = True
        key = serialize(kargs)

        if cls.loop:
            kargs['io_loop'] = cls.loop

        connection = cls.connections.get(key)
        if connection:
            return connection

        cls.connections[key] = AsyncIOMotorClient(**kargs)
        return cls.connections[key]

    @classmethod
    def set_event_loop(cls, loop):
        cls.loop = loop


class MongoDBModel(Model):

    _connection = None
    _database = None
    _collection = None

    @classmethod
    def _connect(cls):
        if cls._connection:
            return

        if cls.__name__ == 'MongoDBModel':
            return

        if not hasattr(cls, 'connection_options'):
            cls.connection_options = { }

        if not hasattr(cls, 'database_options'):
            cls.database_options = { 'name': 'test' }

        if not hasattr(cls, 'collection_options'):
            cls.collection_options = { 'name': cls._table }

        cls._connection = MongoDB.connect(**cls.connection_options)
        cls._database = cls._connection.get_database(**cls.database_options)
        cls._collection = cls._database.get_collection(**cls.collection_options)

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
            raise AttributeError('MongoDBModel primary key type must be: str')

    @classmethod
    async def drop(cls):
        cls._connect()
        await cls._collection.drop()

    @classmethod
    async def exists(cls, id):
        cls._connect()
        document = await cls._collection.find_one(
            { '_id': ObjectId(id) },
            { '_id': True }
        )
        if document:
            return True
        return False

    @classmethod
    async def find_by_id(cls, id):
        cls._connect()
        document = await cls._collection.find_one(
            { '_id': ObjectId(id) }
        )
        if document:
            return cls(document)
        return None

    @classmethod
    async def find_one(cls, *args, **kargs):
        cls._connect()
        document = await cls._collection.find_one(*args, **kargs)
        if document:
            return cls(document)
        return None

    @classmethod
    async def find(cls, *args, **kargs):
        cls._connect()
        cursor = cls._collection.find(*args, **kargs)
        async for document in cursor:
            yield cls(document)

    @classmethod
    async def add(cls, args):
        cls._connect()
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
            message = 'Invalid argument to MongoDBModel.add: must be a list or dict.'
            raise Exception(message)

    async def save(self):
        self._connect()
        self.validate()
        # XXX: should this be replaced with self.exists(self.id)?
        if self.id:
            data = self.serialize(computed=True, controllers=True, reset=True)
            del data['_id']
            document = await self._collection.find_one_and_update(
                { '_id': ObjectId(self.id) },
                { '$set': data },
                return_document=ReturnDocument.AFTER
            )
            if document:
                self.update(document)
            else:
                message = 'No document returned.'
                raise Exception(message)
        else:
            data = self.serialize(computed=True, controllers=True, reset=True)
            result = await self._collection.insert_one(data)
            if result:
                self.id = result.inserted_id
                await self.load()
            else:
                message = 'Inserted ID not available or non-existent.'
                raise Exception(message)

    async def load(self):
        self._connect()
        if self.id:
            document = await self._collection \
                .find_one({ '_id': ObjectId(self.id) })
            if document:
                self.update(document)
            else:
                message = 'No document returned.'
                raise Exception(message)
        else:
            message = 'No document ID, cannot load.'
            raise Exception(message)

    async def delete(self):
        self._connect()
        if self.id:
            result = await self._collection \
                .delete_one({ '_id': ObjectId(self.id) })
            if result:
                if result.deleted_count == 0:
                    message = 'Deleted count is zero.'
                    raise Exception(message)
                else:
                    self._data = { }
            else:
                message = 'Collection operation result is a falsy value.'
                raise Exception(message)
        else:
            message = 'No document ID, cannot delete.'
            raise Exception(message)
