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

    async def operation(self, query):
        raise NotImplemented()

    @classmethod
    async def _connect(cls):

        if cls.__name__ == 'PostgresDBModel':
            return

        if not hasattr(cls, '__connection'):
            cls.__connection__ = {
                'database': 'postgres'
            }

        pool = await PostgresDB.connect(**cls.__connection__)

        async with pool.acquire() as connection:
            try:
                await connection.fetch(f'CREATE TABLE {cls._table} ( data jsonb );')
            except DuplicateTableError:
                pass

        if cls._pool is pool:
            return

        cls._pool = pool

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
        field.computed_empty = True # Compute this field only when empty.
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
        async with await cls._acquire() as connection:
            result = await connection.fetch(f'SELECT data FROM {cls._table} WHERE data->>\'_id\' = \'{id}\';')
            if len(result):
                return cls(loads(result[0]['data']))
            else:
                raise Exception(f'Could not find any data for: {id}')

    @classmethod
    async def find_one(cls, query={ }, **kargs):
        async with await cls._acquire() as connection:
            query_string = f'SELECT data FROM {cls._table} '
            for (key, value) in query.items():
                query_string += f'{key} {value} '
            query_string += f'LIMIT 1;'
            result = await connection.fetch(query_string)
            if len(result):
                return cls(loads(result[0]['data']))
            else:
                raise Exception('No records found.')

    @classmethod
    async def find(cls, query={ }, limit=100, offset=0, **kargs):
        async with await cls._acquire() as connection:
            query_string = f'SELECT data FROM {cls._table} '
            for (key, value) in query.items():
                query_string += f'{key} {value} '
            query_string += f'LIMIT {limit} OFFSET {offset};'
            result = await connection.fetch(query_string)
            for row in result:
                yield cls(loads(row['data']))

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
            raise Exception('Invalid argument to PostgresDBModel.add: must be a list or dict.')

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
