from unittest import TestCase

from sugar_odm import ModelMeta, Field


class ModelMetaTest(TestCase):

    def test_field_repr(self):

        field = Field()
        field.name = 'myfield'

        self.assertEqual(repr(field), '<Field name:myfield>')

    def test_field_str(self):

        field = Field()
        field.name = 'myfield'

        self.assertEqual(str(field), '<Field name:myfield>')

    def test_field_primary_default(self):

        class Test(metaclass=ModelMeta):

            @classmethod
            def default_primary(cls):
                field = Field()
                field.name = 'id'
                return field

        self.assertIs(Test._primary, 'id')

    def test_field_primary_custom(self):

        class Test(metaclass=ModelMeta):
            field = Field(primary=True)

        self.assertIs(Test._primary, 'field')

    def test_field_primary_multiple(self):

        with self.assertRaises(AttributeError):

            class Test(metaclass=ModelMeta):
                alpha = Field(primary=True)
                beta = Field(primary=True)

    def test_field_required(self):

        field = Field(required=True)

        class Test(metaclass=ModelMeta):
            test = field

        self.assertIn(field, Test._required)

    def test_field_model_nested(self):

        class Beta(metaclass=ModelMeta):
            pass

        field = Field(type=Beta)

        class Alpha(metaclass=ModelMeta):
            beta = field

        self.assertIn(field, Alpha._nested)

    def test_field_computed_attribute_missing(self):

        with self.assertRaises(AttributeError):

            class Test(metaclass=ModelMeta):
                field = Field(computed='missing_method')

    def test_field_computed_attribute(self):

        field = Field(computed='method')

        class Test(metaclass=ModelMeta):
            test = field

            def method(self):
                pass

        self.assertIn(field, Test._computed)

    def test_field_computed_function(self):

        field = Field(computed=lambda: None)

        class Test(metaclass=ModelMeta):
            test = field

        self.assertIn(field, Test._computed)

    def test_field_computed_method(self):

        class Beta(object):

            def method(self):
                pass

        beta = Beta()

        field = Field(computed=beta.method)

        class Alpha(metaclass=ModelMeta):
            test = field

        self.assertIn(field, Alpha._computed)

    def test_field_dynamic_attribute_missing(self):

        with self.assertRaises(AttributeError):

            class Test(metaclass=ModelMeta):
                field = Field(type='invalid_method')

    def test_field_dynamic_attribute(self):

        field = Field(type='method')

        class Test(metaclass=ModelMeta):
            test = field

            def method(self):
                pass

        self.assertIn(field, Test._dynamic)

    def test_field_dynamic_function(self):

        field = Field(type=lambda: None)

        class Test(metaclass=ModelMeta):
            test = field

        self.assertIn(field, Test._dynamic)

    def test_field_dynamic_method(self):

        class Beta(object):

            def method(self):
                pass

        field = Field(type=Beta.method)

        class Alpha(metaclass=ModelMeta):
            test = field

        self.assertIn(field, Alpha._dynamic)

    def test_field_invalid_method(self):

        with self.assertRaises(AttributeError):

            class Test(metaclass=ModelMeta):
                field = Field(computed='invalid')

                invalid = 'invalid'

    def test_field_invalid_function(self):

        with self.assertRaises(AttributeError):

            class Test(metaclass=ModelMeta):
                field = Field(computed=10)
