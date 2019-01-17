from unittest import TestCase

from sugar_odm import AsyncTestCase, Field
from sugar_odm.backend.mongodb import MongoDB, MongoDBModel


class MongoDBTest(TestCase):

    def test_connect(self):
        a = MongoDB.connect(host='localhost')
        b = MongoDB.connect(host='localhost')
        c = MongoDB.connect(host='localhost', ssl=False)
        self.assertIs(a, b)
        self.assertIsNot(a, c)


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

    def test_initialize_connection_options_default(self):

        class Test(MongoDBModel):
            pass

        host, port = Test.connection.address

        self.assertEqual(host, 'localhost')
        self.assertEqual(port, 27017)

    def test_initialize_connection_options(self):

        class Test(MongoDBModel):
            connection_options = {
                'host': '127.0.0.1'
            }

        host, port = Test.connection.address

        self.assertEqual(host, '127.0.0.1')

    def test_initialize_connection_options_shared(self):

        class Alpha(MongoDBModel):
            pass

        class Beta(MongoDBModel):
            pass

        class Gamma(MongoDBModel):
            connection_options = { 'host': '127.0.0.1' }

        class Delta(MongoDBModel):
            connection_options = { 'host': '127.0.0.1' }

        self.assertIs(Alpha.connection, Beta.connection)
        self.assertIsNot(Alpha.connection, Gamma.connection)
        self.assertIs(Gamma.connection, Delta.connection)

    def test_initialize_database_options_default(self):

        class Test(MongoDBModel):
            pass

        self.assertEqual(Test.database.name, 'test')

    def test_initialize_database_options(self):

        class Test(MongoDBModel):

            database_options = {
                'name': 'some_database'
            }

        self.assertEqual(Test.database.name, 'some_database')

    def test_initialize_collection_options_default(self):

        class Test(MongoDBModel):
            pass

        self.assertEqual(Test.collection.name, 'tests')

    def test_initialize_collection_options(self):

        class Test(MongoDBModel):
            collection_options = {
                'name': 'some_collection'
            }

        self.assertEqual(Test.collection.name, 'some_collection')

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

    async def test_delete(self):

        class Test(MongoDBModel):
            field = Field()

        test = Test()
        test.field = 'test'

        await test.save()
        await test.delete()

        self.assertDictEqual(test._data, { })

    async def test_exists(self):

        class Test(MongoDBModel):
            pass

        test = Test()
        await test.save()

        id = test.id

        self.assertTrue(await test.exists(id))

        await test.delete()

        self.assertFalse(await test.exists(id))

    async def test_find_one(self):

        class Test(MongoDBModel):
            pass

        test = Test()
        await test.save()

        id = test.id

        test = await Test.find_one(id)

        self.assertEqual(test.id, id)

        await test.delete()

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
