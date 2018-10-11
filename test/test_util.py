from unittest import TestCase

from sanic_jsonapi.util import serialize


class TestUtil(TestCase):

    def test_serialize(self):
        expected = '{"a":"a","b":{"d":"d","e":"e"},"c":"c"}'
        result = serialize({
            'c': 'c',
            'a': 'a',
            'b': { 'e': 'e', 'd': 'd' }
        })
        self.assertEqual(expected, result)
