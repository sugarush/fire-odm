from datetime import datetime

from unittest import TestCase

from fire_odm.util import serialize, inject_query


class TestUtil(TestCase):

    def test_serialize(self):
        expected = '{"a":"a","b":{"d":"d","e":"e"},"c":"c"}'
        result = serialize({
            'c': 'c',
            'a': 'a',
            'b': { 'e': 'e', 'd': 'd' }
        })
        self.assertEqual(expected, result)

    def test_inject_query_date(self):

        query = {
            'datetime': 'Date(2018-10-26)'
        }

        inject_query(query)

        self.assertTrue(isinstance(query['datetime'], datetime))
