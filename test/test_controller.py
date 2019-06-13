from sugar_asynctest import AsyncTestCase

from sugar_odm import MemoryModel, Field


class ControllerTest(AsyncTestCase):

    default_loop = True

    async def test_delete_has_one(self):

        class Alpha(MemoryModel):
            beta = Field(has_one='Beta')

        class Beta(MemoryModel):
            alpha = Field(belongs_to='Alpha', auto_delete=True)

        alpha = Alpha()
        beta = Beta()

        await alpha.save()
        await beta.save()

        alpha.beta = beta
        beta.alpha = alpha

        await alpha.save()
        await beta.save()

        await alpha.delete()

        self.assertIsNone(await Beta.find_one({ 'id': beta.id }))

    async def test_delete_has_many(self):

        class Alpha(MemoryModel):
            beta = Field(has_many='Beta')

        class Beta(MemoryModel):
            alpha = Field(belongs_to='Alpha', auto_delete=True)

        alpha = Alpha()
        beta1 = Beta()
        beta2 = Beta()

        await alpha.save()
        await beta1.save()
        await beta2.save()

        alpha.beta = [ beta1, beta2 ]
        beta1.alpha = alpha
        beta2.alpha = alpha

        await alpha.save()
        await beta1.save()
        await beta2.save()

        await alpha.delete()

        models = [ model async for model in Beta.find() ]

        self.assertEqual([ ], models)
