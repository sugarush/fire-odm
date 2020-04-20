from rethinkdb import RethinkDB
r = RethinkDB()
r.set_loop_type('asyncio')

from .. model import Model
from .. field import Field
from .. util import serialize


class RethinkDB(object):
    '''
    The RethinkDB connection cache.
    '''

    connections = { }

    @classmethod
    async def connect(cls, **kargs):
        key = serialize(kargs)

        connection = cls.connections.get(key)
        if connection:
            return connection

        cls.connections[key] = await r.connect(**kargs)
        return cls.connections[key]

    @classmethod
    async def close(cls):
        for key in cls.connections:
            await cls.connections[key].close()
        cls.connections = { }


class RethinkDBModel(Model):
    '''
    A RethinkDB backed model.
    '''

    _connection = None
    _database = None
    _query = None
    r = None

    async def operation(self, query):
        raise NotImplemented('RethinkDBModel.operation not implemented.')

    @classmethod
    async def _connect(cls):

        if cls.__name__ == 'RethinkDBModel':
            return

        if not hasattr(cls, '__database__'):
            cls.__database__ = {
                'name': 'test'
            }

        if not hasattr(cls, '__connection__'):
            cls.__connection__ = { }

        cls.__connection__.update({
            'db': cls.__database__.get('name')
        })

        connection = await RethinkDB.connect(**cls.__connection__)

        if cls._connection is connection:
            return

        cls._connection = connection

        try:
            cls.r = r
            cls._query = r.table(cls._table)
            cls._database = r.db(cls.__connection__.get('db'))
            await r.table_create(cls._table).run(cls._connection)
        except:
            pass

    @classmethod
    def default_primary(cls):
        field = Field()
        field.name = 'id'
        field.primary = True
        field.type = str
        return field

    @classmethod
    def check_primary(cls, primary):
        if not primary.name is 'id':
            raise AttributeError('MongoDBModel primary key name must be: _id')

        if not primary.type is str:
            raise AttributeError('MongoDBModel primary key type must be: str')

    @classmethod
    async def count(cls):
        await cls._connect()
        return await cls._query.count().run(cls._connection)

    @classmethod
    async def drop(cls):
        await cls._connect()
        return await cls._database.table_drop(cls._table).run(cls._connection)

    @classmethod
    async def exists(cls, id):
        await cls._connect()
        if await cls._query.get_all(id).count().run(cls._connection):
            return True
        return False

    @classmethod
    async def find_by_id(cls, id, **kargs):
        await cls._connect()
        result = await cls._query.get(id).run(cls._connection)
        if result:
            return cls(result)
        return None

    @classmethod
    async def find_one(cls, query={ }, **kargs):
        await cls._connect()
        async for result in await cls._query.filter(query).run(cls._connection):
            return cls(result)

    @classmethod
    async def find(cls, query={ }, **kargs):
        await cls._connect()
        async for result in await cls._query.filter(query).run(cls._connection):
            yield cls(result)

    @classmethod
    async def add(cls, args):
        await cls._connect()
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
            raise Exception('Invalid argument to RethinkDBModel.add: must be a list or dict.')

    async def save(self):
        await self._connect()
        self.validate()
        if self.id and await self.exists(self.id):
            data = self.serialize(computed=True, reset=True)
            del data['id']
            result = await self._query.get(self.id).update(data, return_changes=True).run(self._connection)
            if result:
                self.update(result['changes'][0]['new_val'])
            else:
                message = 'No document returned.'
                raise Exception(message)
        else:
            data = self.serialize(computed=True, reset=True)
            result = await self._query.insert(data, return_changes=True).run(self._connection)
            if result:
                self.update(result['changes'][0]['new_val'])
            else:
                message = 'Inserted ID not available or non-existent.'
                raise Exception(message)

    async def load(self):
        await self._connect()
        if self.id:
            document = await self._query.get(self.id).run(self._connection)
            if document:
                self._data = { }
                self.update(document)
            else:
                message = 'No document returned.'
                raise Exception(message)
        else:
            message = 'No document ID, cannot load.'
            raise Exception(message)

    async def delete(self):
        await self._connect()
        if self.id and self.exists(self.id):
            result = await self._query.get(self.id).delete(return_changes=True).run(self._connection)
            if result['deleted'] == 0:
                message = 'Deleted count is zero.'
                raise Exception(message)
            else:
                self._data = { }
        else:
            message = 'No document ID, cannot delete.'
            raise Exception(message)

    async def changes(self):
        await self._connect()
        if self.id and await self.exists(self.id):
            return await self._query.get(self.id).changes().run(self._connection)
        else:
            message = 'No document ID or document ID does not exist'
            raise Exception(message)
