from uuid import uuid4
from ujson import loads, dumps

from asyncpg import create_pool, DuplicateTableError

from .. util import serialize
from .. model import Model
from .. field import Field


class PostgresDB(object):

    connections = { }
    loop = None

    @classmethod
    async def connect(cls, **kargs):
        key = serialize(kargs)

        connection = cls.connections.get(key)
        if connection:
            return connection

        cls.connections[key] = await create_pool(**kargs)
        return cls.connections[key]

    @classmethod
    async def close(cls):
        for key in cls.connections:
            await cls.connections[key].close()
        cls.connections = { }

    @classmethod
    async def set_event_loop(cls, loop):
        cls.loop = loop
        await cls.close()

class PostgresDBModel(Model):

    _pool = None

    @classmethod
    async def _connect(cls):

        if cls.__name__ == 'PostgresDBModel':
            return

        if not hasattr(cls, '__connection'):
            cls.__connection__ = {
                'database': 'postgres'
            }

        pool = await PostgresDB.connect(**cls.__connection__)

        if cls._pool is pool:
            return

        cls._pool = pool

        async with pool.acquire() as connection:
            try:
                await connection.fetch(f'CREATE TABLE {cls._table} ( data jsonb );')
            except DuplicateTableError:
                pass

    @classmethod
    async def _acquire(cls):
        await cls._connect()
        return cls._pool.acquire()

    @classmethod
    def default_primary(cls):
        field = Field()
        field.name = '_id'
        field.primary = True
        field.type = str
        field.computed = lambda: str(uuid4())
        field.computed_empty = True
        return field

    @classmethod
    def check_primary(cls, primary):
        if not primary.name is '_id':
            raise AttributeError('')

        if not primary.type is str:
            raise AttributeError('')

    @classmethod
    async def count(cls):
        async with await cls._acquire() as connection:
            result = await connection.fetch(f'SELECT count(*) FROM {cls._table};')
            return result[0]['count']

    @classmethod
    async def drop(cls):
        async with await cls._acquire() as connection:
            await connection.fetch(f'DROP TABLE {cls._table};')

    @classmethod
    async def exists(cls, id):
        async with await cls._acquire() as connection:
            result = await connection.fetch(f'SELECT count(*) FROM {cls._table} WHERE data->>\'_id\' = \'{id}\';')
            return result[0]['count']

    @classmethod
    async def find_by_id(cls, id, **kargs):
        pass

    @classmethod
    async def find_one(cls, *args, **kargs):
        pass

    @classmethod
    async def find(cls, *args, **kargs):
        pass

    @classmethod
    async def add(cls, args):
        pass

    async def operation(self, query):
        pass

    async def save(self):
        json = self.serialize(computed=True, reset=True)
        async with await self._acquire() as connection:
            if self.id and await self.exists(self.id):
                result = await connection.fetch(f'UPDATE {self._table} SET data = \'{dumps(json)}\' WHERE data ->> \'_id\' = \'{self.id}\'')
            else:
                result = await connection.fetch(f'INSERT INTO {self._table} VALUES (\'{dumps(json)}\') RETURNING data;')
                self.update(loads(result[0]['data']))

    async def load(self, **kargs):
        if self.id and await self.exists(self.id):
            async with await self._acquire() as connection:
                result = await connection.fetch(f'SELECT data FROM {self._table} WHERE data->>\'_id\' = \'{self.id}\';')
                self.update(loads(result[0]['data']))
        else:
            raise Exception('Missing model id or model id does not exist.')

    async def delete(self):
        if self.id and await self.exists(self.id):
            async with await self._acquire() as connection:
                result = await connection.fetch(f'DELETE FROM {self._table} WHERE data->>\'_id\' = \'{self.id}\' RETURNING data->>\'_id\';')
                deleted_id = result[0].get('?column?')
                if deleted_id == self.id:
                    self._data = { }
                else:
                    raise Exception('Model delete error.')
        else:
            raise Exception('Missing model id or model id does not exist.')
