from unittest import TestCase

from sugar_odm import Query


class QueryTest(TestCase):

    def test_empty(self):
        query = Query('test')
        string, arguments = query.to_postgres()
        self.assertEqual(string, 'SELECT data FROM test LIMIT 100 OFFSET 0;')

    def test_single_field(self):
        query = Query('test', { 'field': 'value' })
        string, arguments = query.to_postgres()

    def test_multi_field(self):
        pass
