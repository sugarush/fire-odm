from unittest import TestCase

from sugar_odm import Model, Field
from sugar_odm.controller.base import ControllerError
from sugar_odm.controller.list import ListController


class TestListController(TestCase):

    def test_init_with_list_type(self):

        class Test(Model):
            field = Field(type=list)

        test = Test()

        self.assertIsInstance(test.field, ListController)

    def test_init_with_list_instance(self):

        class Test(Model):
            field = Field(type=[ ])

        test = Test()

        self.assertEqual(test.field.types, set( ))

    def test_init_with_typed_list_instance(self):

        class Test(Model):
            field = Field(type=[ str, int ])

        test = Test()

        self.assertEqual(test.field.types, set([ str, int ]))

    def test_check_operation_to_empty(self):

        class Test(Model):
            field = Field(type=list)

        test = Test()
        test.field.to_empty = True

        with self.assertRaises(ControllerError):
            test.field._check_operation()

    def test_check_operation_to_replace(self):

        class Test(Model):
            field = Field(type=list)

        test = Test()
        test.field.to_replace = True

        with self.assertRaises(ControllerError):
            test.field._check_operation()

    def test_check_value_untyped(self):

        class Test(Model):
            field = Field(type=list)

        test = Test()
        test.field._check_value(1)

    def test_check_value_typed(self):

        class Test(Model):
            field = Field(type=[ str ])

        test = Test()

        with self.assertRaises(ControllerError):
            test.field._check_value(1)

    def test_check_values_untyped(self):

        class Test(Model):
            field = Field(type=list)

        test = Test()
        test.field._check_values([ 1 ])

    def test_check_values_typed(self):

        class Test(Model):
            field = Field(type=[ str ])

        test = Test()

        with self.assertRaises(ControllerError):
            test.field._check_values([ 1 ])

    def test_check_untyped(self):

        class Test(Model):
            field = Field(type=list)

        test = Test()
        test.field.check([ 1 ])

    def test_check_typed(self):

        class Test(Model):
            field = Field(type=[ str ])

        test = Test()

        with self.assertRaises(ControllerError):
            test.field.check([ 1 ])

    def test_serialize_empty(self):

        class Test(Model):
            field = Field(type=list)

        test = Test(field=[ 1, 2, 3])
        test.field.empty()

        self.assertEqual(test.field.serialize(), [ ])

    def test_serialize_replace(self):

        class Test(Model):
            field = Field(type=list)

        test = Test(field=[ 1, 2, 3])
        test.field = [ 4, 5, 6 ]

        self.assertEqual(test.field.serialize(), [ 4, 5, 6 ])

    def test_serialize_append(self):

        class Test(Model):
            field = Field(type=list)

        test = Test(field=[ 1, 2, 3 ])
        test.field.append(4)

        self.assertEqual(test.field.serialize(), [ 1, 2, 3, 4 ])

    def test_serialize_remove(self):

        class Test(Model):
            field = Field(type=list)

        test = Test(field=[ 1, 2, 3 ])
        test.field.remove(2)

        self.assertEqual(test.field.serialize(), [ 1, 3 ])

    def test_serialize_remove_all(self):

        class Test(Model):
            field = Field(type=list)

        test = Test(field=[ 1, 1, 2, 3, 1, 1 ])
        test.field.remove_all(1)

        self.assertEqual(test.field.serialize(), [ 2, 3 ])

    def test_reset_append(self):

        class Test(Model):
            field = Field(type=list)

        test = Test(field=[ 1, 2, 3 ])
        test.field.append(4)
        test.field.reset()

        self.assertEqual(test.field.serialize(), [ 1, 2, 3 ])

    def test_reset_remove(self):

        class Test(Model):
            field = Field(type=list)

        test = Test(field=[ 1, 2, 3])
        test.field.remove(1)
        test.field.reset()

        self.assertEqual(test.field.serialize(), [ 1, 2, 3])

    def test_reset_remove_all(self):

        class Test(Model):
            field = Field(type=list)

        test = Test(field=[ 1, 1, 2, 3])
        test.field.remove_all(1)
        test.field.reset()

        self.assertEqual(test.field.serialize(), [ 1, 1, 2, 3 ])

    def test_reset_empty(self):

        class Test(Model):
            field = Field(type=list)

        test = Test(field=[ 1, 2, 3])
        test.field.empty()
        test.field.reset()

        self.assertEqual(test.field.serialize(), [ 1, 2, 3 ])

    def test_reset_replace(self):

        class Test(Model):
            field = Field(type=list)

        test = Test(field=[ 1, 2, 3 ])
        test.field = [ 4, 5, 6 ]
        test.field.reset()

        self.assertEqual(test.field.serialize(), [ 1, 2, 3 ])

    def test_operation_empty(self):

        class Test(Model):
            field = Field(type=list)

        test = Test()
        test.field.empty()

        self.assertDictEqual(test.field.operations(), { '$:list:empty': True })

    def test_operation_replace(self):

        class Test(Model):
            field = Field(type=list)

        test = Test(field=[ 1, 2, 3 ])
        test.field = [ 3, 4, 5 ]

        self.assertDictEqual(test.field.operations(), { '$:list:replace': [ 3, 4, 5 ] })

    def test_operation_append(self):

        class Test(Model):
            field = Field(type=list)

        test = Test()
        test.field.append(4)

        self.assertDictEqual(test.field.operations(), { '$:list:append': [ 4 ] })

    def test_operation_remove(self):

        class Test(Model):
            field = Field(type=list)

        test = Test()
        test.field.remove(1)

        self.assertDictEqual(test.field.operations(), { '$:list:remove': [ 1 ] })

    def test_operation_remove_all(self):

        class Test(Model):
            field = Field(type=list)

        test = Test()
        test.field.remove_all(1)

        self.assertDictEqual(test.field.operations(), { '$:list:remove_all': [ 1 ] })
