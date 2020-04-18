from unittest import skip

from sugar_asynctest import AsyncTestCase

from sugar_odm import Model, Field
from sugar_odm.backend.rethink import RethinkDB, RethinkDBModel


class RethinkDBTest(AsyncTestCase):

    default_loop = True

    async def test_connect(self):
        a = await RethinkDB.connect()
        b = await RethinkDB.connect(host='localhost')
        c = await RethinkDB.connect(host='localhost')

        self.assertIs(b, c)
        self.assertIsNot(a, c)

        await RethinkDB.close()


class RethinkDBModelTest(AsyncTestCase):

    default_loop = True

    async def test_save(self):

        class Test(RethinkDBModel):
            field = Field()

        test = Test({ 'field': 'value' })

        await test.save()

        self.assertIsNotNone(self.id)

        await Test.drop()

    async def test_load(self):

        class Test(RethinkDBModel):
            field = Field()

        alpha = Test({ 'field': 'value' })

        await alpha.save()

        beta = Test()
        beta.id = alpha.id
        await beta.load()

        self.assertEqual(alpha.field, beta.field)

        await Test.drop()

    async def test_save_existing(self):

        class Test(RethinkDBModel):
            field = Field()

        alpha = Test({ 'field': 'value' })

        await alpha.save()

        alpha.field = 'alpha'

        await alpha.save()

        self.assertEqual(alpha.field, 'alpha')

        beta = Test()
        beta.id = alpha.id

        await beta.load()

        self.assertEqual(beta.field, 'alpha')

        await Test.drop()

    async def test_add_single(self):

        class Test(RethinkDBModel):
            field = Field()

        await Test.add({ 'field': 'value' })

        self.assertEqual(await Test.count(), 1)

        await Test.drop()

    async def test_add_multiple(self):

        class Test(RethinkDBModel):
            field = Field()

        await Test.add([
            { 'field': 'alpha' },
            { 'field': 'beta'}
        ])

        self.assertEqual(await Test.count(), 2)

        await Test.drop()

    async def test_exists(self):

        class Test(RethinkDBModel):
            field = Field()

        test = Test({ 'field': 'value' })

        await test.save()

        self.assertTrue(await Test.exists(test.id))

        await Test.drop()

    async def test_count(self):

        class Test(RethinkDBModel):
            field = Field()

        await Test.add({ 'field': 'value' })

        self.assertEqual(await Test.count(), 1)

        await Test.drop()

    async def test_drop(self):

        class Test(RethinkDBModel):
            field = Field()

        await Test.add({ 'field': 'value' })

        await Test.drop()

        with self.assertRaises(Exception):
            await Test.count()
