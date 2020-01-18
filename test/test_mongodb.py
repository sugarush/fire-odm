from unittest import TestCase
import asyncio

from fire_asynctest import AsyncTestCase

from fire_odm import Model, Field
from fire_odm.backend.mongodb import MongoDB, MongoDBModel


class MongoDBTest(TestCase):

    def test_connect(self):
        a = MongoDB.connect(host='localhost')
        b = MongoDB.connect(host='localhost')
        c = MongoDB.connect(host='localhost', ssl=False)
        self.assertIs(a, b)
        self.assertIsNot(a, c)

    def test_change_loop(self):
        connection = MongoDB.connect()
        loop = asyncio.get_event_loop()
        MongoDB.set_event_loop(loop)
        self.assertDictEqual(MongoDB.connections, { })


class MongoDBModelTest(AsyncTestCase):

    default_loop = True

    def test_default_primary(self):

        field = MongoDBModel.default_primary()

        self.assertIs(field.type, str)
        self.assertEqual(field.name, '_id')
        self.assertTrue(field.primary)

    def test_check_primary_name(self):

        field = Field()
        field.name = 'test'

        with self.assertRaises(AttributeError):
            MongoDBModel.check_primary(field)

    def test_check_primary_type(self):

        field = Field(type=int)
        field.name = '_id'

        with self.assertRaises(AttributeError):
            MongoDBModel.check_primary(field)

    async def test_connect_connection_options_default(self):

        class Test(MongoDBModel):
            pass

        await Test._connect()

        host, port = Test._connection.address

        self.assertEqual(host, 'localhost')
        self.assertEqual(port, 27017)

    async def test_connect_connection_options(self):

        class Test(MongoDBModel):
            __connection__ = {
                'host': '127.0.0.1'
            }

        await Test._connect()

        host, port = Test._connection.address

        self.assertEqual(host, '127.0.0.1')

    async def test_connect_connection_options_shared(self):

        class Alpha(MongoDBModel):
            pass

        class Beta(MongoDBModel):
            pass

        class Gamma(MongoDBModel):
            __connection__ = { 'host': '127.0.0.1' }

        class Delta(MongoDBModel):
            __connection__ = { 'host': '127.0.0.1' }

        await Alpha._connect()
        await Beta._connect()
        await Gamma._connect()
        await Delta._connect()

        self.assertIs(Alpha._connection, Beta._connection)
        self.assertIsNot(Alpha._connection, Gamma._connection)
        self.assertIs(Gamma._connection, Delta._connection)

    async def test_connect_database_options_default(self):

        class Test(MongoDBModel):
            pass

        await Test._connect()

        self.assertEqual(Test._database.name, 'test')

    async def test_connect_database_options(self):

        class Test(MongoDBModel):

            __database__ = {
                'name': 'some_database'
            }

        await Test._connect()

        self.assertEqual(Test._database.name, 'some_database')

    async def test_connect_collection_options_default(self):

        class Test(MongoDBModel):
            pass

        await Test._connect()

        self.assertEqual(Test._collection.name, 'tests')

    async def test_connect_collection_options(self):

        class Test(MongoDBModel):
            __collection__ = {
                'name': 'some_collection'
            }

        await Test._connect()

        self.assertEqual(Test._collection.name, 'some_collection')

    async def test_save_new(self):

        class Test(MongoDBModel):
            pass

        test = Test()

        await test.save()

        self.assertTrue(test.id)

        await test.delete()

    async def test_save_existing(self):

        class Test(MongoDBModel):
            field = Field()

        test = Test()
        test.field = 'test'

        await test.save()

        self.assertEqual(test.field, 'test')

        test.field = 'test2'

        await test.save()

        self.assertEqual(test.field, 'test2')

        await test.delete()

    async def test_load(self):

        class Test(MongoDBModel):
            field = Field()

        test = Test()
        test.field = 'test'

        await test.save()

        id = test.id

        test = Test()
        test.id = id

        await test.load()

        self.assertEqual(test.field, 'test')

        await test.delete()

    async def test_load_with_projection(self):

        class Alpha(Model):
            field = Field()

        class Beta(MongoDBModel):
            alpha = Field(type=Alpha)
            field = Field()

        beta = Beta()
        beta.alpha = { 'field': 'testing' }
        beta.field = 'value'

        await beta.save()

        id = beta.id

        beta = Beta()
        beta.id = id

        await beta.load(projection={
            'alpha.field': 1
        })

        self.assertIsNone(beta.field)
        self.assertEqual(beta.alpha.field, 'testing')

        await beta.delete()

    async def test_delete(self):

        class Test(MongoDBModel):
            field = Field()

        test = Test()
        test.field = 'test'

        await test.save()
        await test.delete()

        self.assertDictEqual(test._data, { })

    async def test_count(self):

        class Test(MongoDBModel):
            pass

        await Test.drop()

        await Test.add([
            { },
            { },
            { }
        ])

        self.assertEqual(await Test.count(), 3)

    async def test_exists(self):

        class Test(MongoDBModel):
            pass

        test = Test()
        await test.save()

        id = test.id

        self.assertTrue(await test.exists(id))

        await test.delete()

        self.assertFalse(await test.exists(id))

    async def test_find_by_id(self):

        class Test(MongoDBModel):
            pass

        test = Test()
        await test.save()

        id = test.id

        test = await Test.find_by_id(id)

        self.assertEqual(test.id, id)

        await test.delete()

    async def test_find_by_id_no_document_returned(self):

        class Test(MongoDBModel):
            pass

        test = await Test.find_by_id('1234567890abcdefabcdefab')

        self.assertIs(test, None)

    async def test_find_by_id_with_projection(self):

        class Alpha(Model):
            field = Field()

        class Beta(MongoDBModel):
            alpha = Field(type=Alpha)
            field = Field()

        beta = Beta()
        beta.alpha = { 'field': 'testing' }
        beta.field = 'value'

        await beta.save()

        beta = await Beta.find_by_id(beta.id, projection={
            'alpha.field': 1
        })

        self.assertIsNone(beta.field)
        self.assertEqual(beta.alpha.field, 'testing')

    async def test_find_one(self):

        class Test(MongoDBModel):
            field = Field()

        test = Test()
        test.field = 'alpha'
        await test.save()

        test = await Test.find_one({ 'field': 'alpha' })

        self.assertEqual(test.field, 'alpha')

        await test.delete()

    async def test_find_one_no_document_returned(self):

        class Test(MongoDBModel):
            pass

        test = await Test.find_one({ 'nonexistent': 'field' })

        self.assertIs(test, None)

    async def test_find_one_with_projection(self):

        class Alpha(Model):
            field = Field()

        class Beta(MongoDBModel):
            alpha = Field(type=Alpha)
            field = Field()

        beta = Beta()
        beta.alpha = { 'field': 'testing' }
        beta.field = 'value'

        await beta.save()

        beta = await Beta.find_one({ 'field': 'value' }, projection = {
            'alpha.field': 1
        })

        self.assertIsNone(beta.field)
        self.assertEqual(beta.alpha.field, 'testing')

        await beta.delete()

    async def test_find(self):

        class Test(MongoDBModel):
            pass

        test1 = Test()
        await test1.save()

        test2 = Test()
        await test2.save()

        ids = [ ]

        async for model in Test.find():
            ids.append(model.id)
            await model.delete()

        self.assertIn(test1.id, ids)
        self.assertIn(test2.id, ids)

        await Test.drop()

    async def test_find_with_projection(self):

        class Alpha(Model):
            field = Field()

        class Beta(MongoDBModel):
            alpha = Field(type=Alpha)
            field = Field()

        await Beta.drop()

        beta1 = Beta()
        beta1.alpha = { 'field': 'testing' }
        beta1.field = 'value'

        await beta1.save()

        beta2 = Beta()
        beta2.alpha = { 'field': '123' }
        beta2.field = 'value'

        await beta2.save()

        async for beta in Beta.find(projection={
            'alpha.field': 1
        }):
            self.assertIsNone(beta.field)
            self.assertIsNotNone(beta.alpha.field)

        await Beta.drop()

    async def test_add_single(self):

        class Test(MongoDBModel):
            pass

        model = await Test.add({ })

        self.assertTrue(model.id)

        await model.delete()

    async def test_add_multiple(self):

        class Test(MongoDBModel):
            pass

        models = await Test.add([
            { },
            { },
            { }
        ])

        self.assertEqual(len(models), 3)

    async def test_add_invalid(self):

        class Test(MongoDBModel):
            pass

        with self.assertRaises(Exception):
            await Test.add('invalid')

    async def test_drop(self):

        class Test(MongoDBModel):
            pass

        models = await Test.add([
            { },
            { },
            { }
        ])

        id = models[0].id

        await Test.drop()

        self.assertFalse(await Test.exists(id))

    async def test_operation(self):

        class Test(MongoDBModel):
            field = Field(type=int)

        await Test.drop()

        test = Test(field=1)
        await test.save()

        await test.operation({ '$inc': { 'field': 1 } })

        self.assertEqual(test.field, 2)
