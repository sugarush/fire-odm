from unittest import TestCase

from bson import ObjectId

from sanic_jsonapi import AsyncTestCase, Field
from sanic_jsonapi.backend.mongodb import MongoDB, MongoDBModel


class MongoDBTest(TestCase):

    def test_connect(self):
        a = MongoDB.connect(host='localhost')
        b = MongoDB.connect(host='localhost')
        c = MongoDB.connect(host='localhost', ssl=False)
        self.assertIs(a, b)
        self.assertIsNot(a, c)


class MongoDBModelTest(AsyncTestCase):

    def test_default_primary(self):

        field = MongoDBModel.default_primary()

        self.assertIs(field.type, ObjectId)
        self.assertEqual(field.name, '_id')
        self.assertTrue(field.primary)

    def test_check_primary_name(self):

        field = Field()
        field.name = 'test'

        with self.assertRaises(AttributeError):
            MongoDBModel.check_primary(field)

    def test_check_primary_type(self):

        field = Field(type=str)
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

    def test_save_new(self):
        pass

    def test_save_existing(self):
        pass

    def test_exists(self):
        pass
