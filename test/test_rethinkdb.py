from unittest import skip

import rethinkdb as r

from sanic_jsonapi import AsyncTestCase, Field, Error
from sanic_jsonapi.backend.rethinkdb import RethinkDBModel, RethinkDB


class RethinkDBConnectionTest(AsyncTestCase):

    async def test_connect(self):
        c = await RethinkDB.connect(db='test') #ssl={'cacerts': ''})
        self.assertTrue(c.is_open())
        await RethinkDB.close()

    async def test_connect_multiple(self):
        a = await RethinkDB.connect(db='test')
        b = await RethinkDB.connect(db='test')
        c = await RethinkDB.connect(db='testing')
        self.assertIs(a, b)
        self.assertIsNot(a, c)
        await RethinkDB.close()

    async def test_close(self):
        a = await RethinkDB.connect(db='test')
        b = await RethinkDB.connect(db='testing')
        await RethinkDB.close()
        self.assertFalse(a.is_open())
        self.assertFalse(b.is_open())


class RethinkDBModelTest(AsyncTestCase):

    @skip
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

    @skip
    async def test_ensure_database(self):

        class Test(RethinkDBModel):
            db_options = { 'db': 'testdb' }

        await Test.connect()

        databases = await r.db_list().run(Test.connection)

        self.assertIn('testdb', databases)

        await Test.drop()
        await r.db_drop('testdb').run(Test.connection)
        await Test.close()

    @skip
    async def test_ensure_table(self):

        class Test(RethinkDBModel):
            pass

        await Test.connect()

        tables = await Test._db.table_list().run(Test.connection)

        self.assertIn(Test._table, tables)

        await Test.drop()
        await Test.close()

    @skip
    async def test_ensure_indexes(self):

        class Beta(RethinkDBModel):
            field = Field(indexed=True)

        class Alpha(RethinkDBModel):
            beta = Field(type=Beta)
            field = Field(indexed=True)

    async def test_save_new(self):

        class Test(RethinkDBModel):
            pass

        await Test.drop()

        test = Test()

        self.assertFalse(test.id)

        error = await test.save()

        self.assertEqual(error, None)

        self.assertTrue(test.id)

        await Test.drop()
        await Test.close()

    async def test_save_existing(self):

        class Test(RethinkDBModel):
            field = Field()

        await Test.drop()

        test = Test({ 'field': 'value' })

        error = await test.save()

        self.assertEqual(error, None)

        test.field = 'new_value'

        error = await test.save()

        self.assertEqual(error, None)

        self.assertEqual(test.field, 'new_value')

        await Test.drop()
        await Test.close()

    async def test_save_invalid(self):

        class Test(RethinkDBModel):
            field = Field(required=True)

        await Test.drop()

        test = Test()

        error = await test.save()

        self.assertIsInstance(error, Error)

        await Test.drop()
        await Test.close()

    @skip
    async def test_add_with_primary_key_default(self):

        class Test(RethinkDBModel):
            field = Field()

        await Test.drop()

        model, error = await Test.add({ 'field': 'value' })

        self.assertIs(error, None)
        self.assertTrue(model.id)

        await Test.drop()
        await Test.close()

    @skip
    async def test_add_with_primary_key_custom(self):

        class Test(RethinkDBModel):
            primary = Field(primary=True)

        await Test.drop()

        model, error = await Test.add({ 'primary': 'value' })

        self.assertIs(error, None)
        self.assertEqual(model.id, 'value')

        await Test.drop()
        await Test.close()

    @skip
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

    @skip
    async def test_add_duplicate_primary(self):

        class Test(RethinkDBModel):
            field = Field()
