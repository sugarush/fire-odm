from sugar_asynctest import AsyncTestCase

from sugar_odm import PostgresDBModel, Field


class PostgresDBFindTest(AsyncTestCase):

    default_loop = True

    async def test_find_one_single_field(self):

        class Test(PostgresDBModel):
            alpha = Field()
            beta = Field()

        await Test.add({ 'alpha': 'a' })

        model = await Test.find_one({ 'alpha': 'a' })

        self.assertEqual(model.alpha, 'a')

        await Test.drop()

    async def test_find_one_multi_field(self):

        class Test(PostgresDBModel):
            alpha = Field()
            beta = Field()

        await Test.add([{ 'alpha': 'a' }, { 'alpha': 'a', 'beta': 'b' }])

        model = await Test.find_one({ 'alpha': 'a', 'beta': 'b' })

        self.assertEqual(model.alpha, 'a')
        self.assertEqual(model.beta, 'b')

        await Test.drop()

    async def test_find_single_field(self):

        class Test(PostgresDBModel):
            alpha = Field()
            beta = Field()

        await Test.add({ 'alpha': 'a' })

        models = [ model async for model in Test.find({ 'alpha': 'a' }) ]

        self.assertEqual(len(models), 1)

        await Test.drop()

    async def test_find_multi_field(self):

        class Test(PostgresDBModel):
            alpha = Field()
            beta = Field()

        await Test.add([{ 'alpha': 'a' }, { 'alpha': 'a', 'beta': 'b' }])

        models = [ model async for model in Test.find({ 'alpha': 'a', 'beta': 'b' }) ]

        self.assertEqual(models[0].alpha, 'a')
        self.assertEqual(models[0].beta, 'b')
        self.assertEqual(len(models), 1)

        await Test.drop()
