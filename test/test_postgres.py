import asyncio
from unittest import skip

from sugar_asynctest import AsyncTestCase

from sugar_odm import PostgresDB, PostgresDBModel, Field


class PostgresDBTest(AsyncTestCase):

    default_loop = True

    async def test_connect(self):
        a = await PostgresDB.connect(host='localhost', database='postgres')
        b = await PostgresDB.connect(host='localhost', database='postgres')
        c = await PostgresDB.connect(host='localhost', database='postgres', port=5432)

        self.assertIs(a, b)
        self.assertIsNot(a, c)

    async def test_change_loop(self):
        connection = await PostgresDB.connect(host='localhost', database='postgres')
        loop = asyncio.get_event_loop()
        await PostgresDB.set_event_loop(loop)
        self.assertDictEqual(PostgresDB.connections, { })


class PostgresDBModelTest(AsyncTestCase):

    default_loop = True

    def test_default_primary(self):

        field = PostgresDBModel.default_primary()

        self.assertIs(field.type, str)
        self.assertEqual(field.name, '_id')
        self.assertTrue(field.primary)

    def test_check_primary_name(self):

        field = Field()
        field.name = 'test'

        with self.assertRaises(AttributeError):
            PostgresDBModel.check_primary(field)

    def test_check_primary_type(self):

        field = Field(type=int)
        field.name = '_id'

        with self.assertRaises(AttributeError):
            PostgresDBModel.check_primary(field)

    async def test_connect_pool_options_shared(self):

        class Alpha(PostgresDBModel):
            pass

        class Beta(PostgresDBModel):
            pass

        class Gamma(PostgresDBModel):
            __connection__ = { 'host': 'localhost' }

        class Delta(PostgresDBModel):
            __connection__ = { 'host': 'localhost' }

        await Alpha._connect()
        await Beta._connect()
        await Gamma._connect()
        await Delta._connect()

        self.assertIs(Alpha._pool, Beta._pool)
        self.assertIsNot(Alpha._pool, Gamma._pool)
        self.assertIs(Gamma._pool, Delta._pool)

    async def test_count(self):

        class Test(PostgresDBModel):
            pass

        await Test.add([{ }, { }])

        self.assertEqual(await Test.count(), 2)

        await Test.drop()

    async def test_add_single(self):

        class Test(PostgresDBModel):
            pass

        model = await Test.add({ })

        self.assertIsNotNone(model.id)

        await Test.drop()

    async def test_add_multiple(self):

        class Test(PostgresDBModel):
            pass

        models = await Test.add([ { }, { } ])

        [ self.assertIsNotNone(model.id) for model in models ]

        await Test.drop()

    async def test_drop(self):

        class Test(PostgresDBModel):
            pass

        await Test.add({ })

        self.assertEqual(await Test.count(), 1)

        await Test.drop() # this removes the table from the database

        class Test(PostgresDBModel): # this recreates the table in the database
            pass

        self.assertEqual(await Test.count(), 0)

    async def test_exists(self):

        class Test(PostgresDBModel):
            pass

        model = await Test.add({ })

        self.assertTrue(await Test.exists(model.id))

        await Test.drop()

    async def test_find_by_id(self):

        class Test(PostgresDBModel):
            pass

        alpha = await Test.add({ })
        beta = await Test.find_by_id(alpha.id)

        self.assertEqual(alpha.id, beta.id)

        await Test.drop()

    async def test_find_one_no_query(self):

        class Test(PostgresDBModel):
            field = Field()

        await Test.add([{ 'field': 'alpha' }, { 'field': 'beta' }])

        model = await Test.find_one()

        self.assertIsNotNone(model.id)

        await Test.drop()

    async def test_find_one_query(self):

        class Test(PostgresDBModel):
            field = Field()

        await Test.add([{ 'field': 'alpha' }, { 'field': 'beta' }])

        model = await Test.find_one({ 'field': 'beta' })

        self.assertEqual(model.field, 'beta')

        await Test.drop()

    async def test_find_no_query(self):

        class Test(PostgresDBModel):
            field = Field()

        await Test.add([{ 'field': 'alpha' }, { 'field': 'beta' }])

        models = [ model async for model in Test.find() ]

        self.assertEqual(len(models), 2)

        await Test.drop()

    async def test_find_query(self):

        class Test(PostgresDBModel):
            field = Field()

        await Test.add([{ 'field': 'alpha' }, { 'field': 'beta' }])

        models = [ model async for model in Test.find({ 'field': 'alpha' }) ]

        self.assertEqual(len(models), 1)

        await Test.drop()

    async def test_save_new(self):

        class Test(PostgresDBModel):
            field = Field()

        model = Test({ 'field': 'value' })

        self.assertIsNone(model.id)

        await model.save()

        self.assertIsNotNone(model.id)

        await Test.drop()

    async def test_save_update(self):

        class Test(PostgresDBModel):
            field = Field()

        model = Test({ 'field': 'value' })

        await model.save()

        model.field = '12345'

        await model.save()

        self.assertEqual(model.field, '12345')

        await Test.drop()

    async def test_save_update_with_quote(self):

        class Test(PostgresDBModel):
            field = Field()

        model = Test({ 'field': 'value' })

        await model.save()

        model.field = "a string with a ' "

        await model.save()

        self.assertEqual(model.field, "a string with a ' ")

        await Test.drop()

    async def test_load(self):

        class Test(PostgresDBModel):
            field = Field()

        alpha = await Test.add({ 'field': 'value' })

        beta = Test({ '_id': alpha.id })

        await beta.load()

        self.assertEqual(beta.field, 'value')

        await Test.drop()

    async def test_delete(self):

        class Test(PostgresDBModel):
            pass

        model = await Test.add({ })

        self.assertEqual(await Test.count(), 1)

        await model.delete()

        self.assertEqual(await Test.count(), 0)

        await Test.drop()
