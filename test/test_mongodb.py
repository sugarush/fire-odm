from unittest import TestCase

from sanic_jsonapi import AsyncTestCase
from sanic_jsonapi.backend.mongodb import MongoDB, MongoDBModel


class MongoDBConnection(TestCase):

    def test_connect(self):
        a = MongoDB.connect(host='localhost')
        b = MongoDB.connect(host='localhost')
        c = MongoDB.connect(host='localhost', ssl=False)
        self.assertIs(a, b)
        self.assertIsNot(a, c)


class MongoDBModel(AsyncTestCase):

    def test_default_primary(self):

        class Test(MongoDBModel):
            pass

        field = Test.default_primary()

        print(field)
