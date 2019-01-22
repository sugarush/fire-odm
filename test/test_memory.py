from sugar_asynctest import AsyncTestCase

from sugar_odm import Field
from sugar_odm.backend.memory import MemoryModel


class MemoryModelTest(AsyncTestCase):

    default_loop = True

    async def test_save_new(self):

        class Test(MemoryModel):
            pass

        test = Test()

        await test.save()

        self.assertTrue(test.id)

    async def test_save_existing(self):

        class Test(MemoryModel):
            pass

        test = Test()

        await test.save()

        id = test.id

        await test.save()

        self.assertEqual(test.id, id)

    async def test_load(self):

        class Test(MemoryModel):
            field = Field()

        test1 = Test()
        test1.field = 'value'

        await test1.save()

        id = test1.id

        test2 = Test()
        test2.id = id

        await test2.load()

        self.assertEqual(test2.field, 'value')

    async def test_load_missing(self):

        class Test(MemoryModel):
            pass

        test = Test()

        await test.save()

        await Test.drop()

        with self.assertRaises(Exception):
            await test.load()

    async def test_load_no_id(self):

        class Test(MemoryModel):
            pass

        test = Test()

        with self.assertRaises(Exception):
            await test.load()

    async def test_delete(self):

        class Test(MemoryModel):
            pass

        test = Test()

        await test.save()

        id = test.id

        await test.delete()

        self.assertDictEqual(test._data, { })
        self.assertTrue(id not in Test.db)

    async def test_delete_missing(self):

        class Test(MemoryModel):
            pass

        test = Test()

        await test.save()

        await Test.drop()

        with self.assertRaises(Exception):
            await test.delete()

    async def test_delete_no_id(self):

        class Test(MemoryModel):
            pass

        test = Test()

        with self.assertRaises(Exception):
            await test.delete()

    async def test_add_dict(self):

        class Test(MemoryModel):
            pass

        test = await Test.add({ })

        self.assertTrue(test.id)

    async def test_add_list(self):

        class Test(MemoryModel):
            pass

        tests = await Test.add([
            { },
            { },
            { }
        ])

        self.assertEqual(len(tests), 3)

    async def test_add_invalid(self):

        class Test(MemoryModel):
            pass

        with self.assertRaises(Exception):

            await Test.add('invalid')

    async def test_exists(self):

        class Test(MemoryModel):
            pass

        test = Test()

        await test.save()

        self.assertTrue(await Test.exists(test.id))
        self.assertFalse(await Test.exists('non-existent'))

    async def test_drop(self):

        class Test(MemoryModel):
            pass

        test = Test()

        await test.save()

        await Test.drop()

        self.assertEqual(len(Test.db), 0)

    async def test_find_by_id(self):

        class Test(MemoryModel):
            pass

        test1 = Test()

        await test1.save()

        test2 = await Test.find_by_id(test1.id)

        self.assertEqual(test1.id, test2.id)

    async def test_find_by_id_non_existent(self):

        class Test(MemoryModel):
            pass

        test = await Test.find_by_id('non-existent')

        self.assertIsNone(test)

    async def test_find(self):

        class Test(MemoryModel):
            pass

        tests = await Test.add([
            { },
            { },
            { }
        ])

        count = 0

        async for model in Test.find():
            count += 1

        self.assertEqual(count, 3)

    async def test_find_one(self):

        class Test(MemoryModel):
            field = Field()

        await Test.add([
            { 'field': 'value' },
            { 'field': 'value' }
        ])

        test = await Test.find_one({ 'field': 'value' })

        self.assertTrue(test)
