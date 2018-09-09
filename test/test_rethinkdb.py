import rethinkdb as r

from sanic_jsonapi import AsyncTestCase, Field
from sanic_jsonapi.rethinkdb import RethinkDBModel, Connection


class DatabaseTest(AsyncTestCase):

    def test_hash(self):
        expected = '{"a":"a","b":{"d":"d","e":"e"},"c":"c"}'
        result = Connection._hash({
            'c': 'c',
            'a': 'a',
            'b': { 'e': 'e', 'd': 'd' }
        })
        self.assertEqual(expected, result)

    async def test_connect(self):
        c = await Connection.connect(db='test') #ssl={'cacerts': ''})
        self.assertTrue(c.is_open())
        await Connection.close()

    async def test_connect_multiple(self):
        a = await Connection.connect(db='test')
        b = await Connection.connect(db='test')
        c = await Connection.connect(db='testing')
        self.assertIs(a, b)
        self.assertIsNot(a, c)
        await Connection.close()

    async def test_close(self):
        a = await Connection.connect(db='test')
        b = await Connection.connect(db='testing')
        await Connection.close()
        self.assertFalse(a.is_open())
        self.assertFalse(b.is_open())


class RethinkDBModelTest(AsyncTestCase):

    async def test_connect_and_close(self):

        class Test(RethinkDBModel):
            db_options = { 'db': 'testdb' }

        await Test.connect()
        a = Test.connection

        await Test.connect()
        b = Test.connection

        self.assertTrue(Test.connection)
        self.assertTrue(Test.connection.is_open())
        self.assertIs(a, b)

        await Test.drop()
        await Test.close()

        self.assertFalse(Test.connection.is_open())

    async def test_ensure_database(self):

        class Test(RethinkDBModel):
            db_options = { 'db': 'testdb' }

        await Test.connect()

        databases = await r.db_list().run(Test.connection)

        self.assertIn('testdb', databases)

        await Test.drop()
        await r.db_drop('testdb').run(Test.connection)
        await Test.close()

    async def test_ensure_table(self):

        class Test(RethinkDBModel):
            pass

        await Test.connect()

        tables = await Test._db.table_list().run(Test.connection)

        self.assertIn(Test._table, tables)

        await Test.drop()
        await Test.close()

    async def test_ensure_indexes(self):

        class Beta(RethinkDBModel):
            field = Field(indexed=True)

        class Alpha(RethinkDBModel):
            beta = Field(type=Beta)
            field = Field(indexed=True)

    async def test_save(self):

        from datetime import datetime

        class Beta(RethinkDBModel):
            timestamp = Field(computed='get_timestamp')

            def get_timestamp(self):
                return datetime.utcnow().timestamp()

        class Alpha(RethinkDBModel):
            name = Field()
            beta = Field(type=Beta)

        await Alpha.drop()

        alpha = Alpha()

        await alpha.save()
        print(alpha.id, alpha.beta.timestamp)

    async def test_add_with_primary_key_default(self):

        class Test(RethinkDBModel):
            field = Field()

        await Test.drop()

        model, error = await Test.add({ 'field': 'value' })

        self.assertIs(error, None)
        self.assertTrue(model.id)

        await Test.drop()
        await Test.close()

    async def test_add_with_primary_key_custom(self):

        class Test(RethinkDBModel):
            primary = Field(primary=True)

        await Test.drop()

        model, error = await Test.add({ 'primary': 'value' })

        self.assertIs(error, None)
        self.assertEqual(model.id, 'value')

        await Test.drop()
        await Test.close()

    async def test_add_multiple(self):

        class Test(RethinkDBModel):
            field = Field()

        await Test.drop()

        models, errors = await Test.add([
            {
                'field': 'value_one'
            },
            {
                'field': 'value_two'
            }
        ])

        self.assertFalse(errors)

        for model in models:
            self.assertTrue(model.id)

        await Test.drop()
        await Test.close()

    async def test_add_duplicate_primary(self):
        pass
