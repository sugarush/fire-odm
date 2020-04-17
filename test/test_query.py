from unittest import TestCase

from sugar_odm import Query


class QueryTest(TestCase):

    def test_empty(self):
        query = Query('test')
        string, arguments = query.to_postgres()
        self.assertEqual(string, 'SELECT data FROM test LIMIT 100 OFFSET 0;')
        self.assertEqual(len(arguments), 0)

    def test_single_field(self):
        query = Query('test', { 'field': 'value' })
        string, arguments = query.to_postgres()
        self.assertEqual(len(arguments), 2)
        self.assertEqual(string, 'SELECT data FROM test WHERE data->>$1 = $2 LIMIT 100 OFFSET 0;')

    def test_multi_field(self):
        query = Query('test', { 'alpha': 'a', 'beta': 'b' })
        string, arguments = query.to_postgres()
        self.assertEqual(len(arguments), 4)
        self.assertEqual(string, 'SELECT data FROM test WHERE (data->>$1 = $2 AND data->>$3 = $4) LIMIT 100 OFFSET 0;')
