from unittest import TestCase

from sanic_jsonapi import Model, Field, Error


class ModelTest(TestCase):

    def test_repr(self):

        class Test(Model):
            pass

        test = Test()

        self.assertEqual(repr(test), '{}')

    def test_str(self):

        class Test(Model):
            pass

        test = Test()

        self.assertEqual(str(test), '{}')

    def test_check_undefined(self):

        class Test(Model):
            pass

        test = Test()

        with self.assertRaises(Error):
            test._check_undefined({ 'field': 'value' })

    def test_check_missing(self):

        class Test(Model):
            field = Field(required=True)

        test = Test()

        with self.assertRaises(Error):
            test._check_missing({ })

    def test_check_field(self):

        class Test(Model):
            field = Field()

        test = Test()

        field = test._check_field('field')
        self.assertTrue(field)

        with self.assertRaises(Error):
            test._check_field('undefined')

    def test_set(self):

        class Test(Model):
            field = Field()

        test = Test()
        test._set('field', 'value')

        self.assertIs(test.field, 'value')

    def test_set_undefined(self):

        class Test(Model):
            pass

        test = Test()

        with self.assertRaises(Error):
            test._set('field', 'value')

    def test_set_nested_model_from_dict(self):

        class Beta(Model):
            field = Field()

        class Alpha(Model):
            beta = Field(type=Beta)

        alpha = Alpha()
        alpha._set('beta', { 'field': 'value' })

        self.assertIs(alpha.beta.field, 'value')

    def test_set_nested_model_from_model(self):
        class Beta(Model):
            field = Field()

        class Alpha(Model):
            beta = Field(type=Beta)

        alpha = Alpha()
        alpha._set('beta', Beta({ 'field': 'value' }))

        self.assertIs(alpha.beta.field, 'value')

    def test_set_multiple_nested(self):

        class Gamma(Model):
            field = Field()

        class Beta(Model):
            gamma = Field(type=Gamma)

        class Alpha(Model):
            beta = Field(type=Beta)

        alpha = Alpha()
        alpha._set('beta', { 'gamma': { 'field': 'value' } })

        self.assertIs(alpha.beta.gamma.field, 'value')

    def test_set_keyword(self):

        class Test(Model):
            field = Field()

        test = Test()
        test.set(field='value')

        self.assertIs(test.field, 'value')

    def test_set_dictionary(self):

        class Test(Model):
            field = Field()

        test = Test()
        test.set({ 'field': 'value' })

        self.assertIs(test.field, 'value')

    def test_set_dictionary_and_keyword(self):

        class Test(Model):
            alpha = Field()
            beta = Field()

        test = Test()
        test.set({ 'alpha': 'a', 'beta': 'b' }, beta='value')

        self.assertIs(test.alpha, 'a')
        self.assertIs(test.beta, 'value')

    def test_setattr(self):

        class Test(Model):
            field = Field()

        test = Test()
        test.field = 'value'

        self.assertIs(test.field, 'value')

    def test_setattr_with_nested_model(self):

        class Beta(Model):
            name = Field()

        class Alpha(Model):
            field = Field()
            beta = Field(type=Beta)

        alpha = Alpha()

        with self.assertRaises(Error):
            alpha.beta = 'invalid'

        alpha.beta = { }

        self.assertIs(type(alpha.beta), Beta)

        alpha.beta = Beta()

        self.assertIs(type(alpha.beta), Beta)

    def test_getattr(self):

        class Test(Model):
            field = Field()

        test = Test()

        self.assertIs(test.field, None)

        with self.assertRaises(AttributeError):
            self.not_a_field

    def test_id_setter_and_getter(self):

        class Test(Model):
            pass

        test = Test()

        test.id = '1'

        self.assertIs(test.id, '1')

    def test_validate(self):

        class Test(Model):
            field = Field(required=True)

        test = Test()

        with self.assertRaises(Error):
            test.validate()

        test.field = 'value'

        test.validate()

    def test_validate_nested_required(self):

        class Beta(Model):
            field = Field(required=True)

        class Alpha(Model):
            beta = Field(type=Beta)

        alpha = Alpha()

        with self.assertRaises(Error):
            alpha.validate()

    def test_serialize(self):

        expected = {'value': 'string', 'object': {'alpha': 'a', 'beta': 'b'}}

        class Test(Model):
            value = Field()
            object = Field(type=dict)

        test = Test()
        test.value = 'string'
        test.object = { 'alpha': 'a', 'beta': 'b' }

        self.assertEqual(test.serialize(), expected)

    def test_serialize_nested_model(self):

        expected = {'beta': {'value': 'test'}}

        class Beta(Model):
            value = Field()

        class Alpha(Model):
            beta = Field(type=Beta)

        alpha = Alpha()
        alpha.beta = { 'value': 'test' }

        self.assertEqual(alpha.serialize(), expected)

    def test_serialize_computed_function(self):

        class Test(Model):
            computed = Field(type=str, computed=lambda: 'value')

        test = Test()
        self.assertIs(test.serialize(compute=True)['computed'], 'value')

    def test_serialize_computed_method(self):

        class Test(Model):
            computed = Field(type=str, computed='get_hello')

            def get_hello(self):
                return 'hello'

        test = Test()
        self.assertIs(test.serialize(compute=True)['computed'], 'hello')

    def test_serialize_computed_empty(self):

        class Test(Model):
            computed = Field(type=str, computed='get_hello', computed_empty=True)

            def get_hello(self):
                return 'hello'

        test = Test()

        self.assertIs(test.serialize(compute=True)['computed'], 'hello')

        test.computed = 'value'

        self.assertIs(test.serialize()['computed'], 'value')

    def test_serialize_computed_type(self):

        class Test(Model):
            computed = Field(type=dict, computed='get_hello', computed_type=True)

            def get_hello(self):
                return 'hello'

        test = Test()

        with self.assertRaises(Error):
            test.computed = 'value'

        self.assertIs(test.serialize(compute=True)['computed'], 'hello')
