from sugar_asynctest import AsyncTestCase

from sugar_odm import MongoDBModel, Field
from sugar_odm import MongoDB


class ControllerTest(AsyncTestCase):

    default_loop = True

    async def test_has_many_push(self):

        class Alpha(MongoDBModel):
            beta = Field(has_many='Beta')

        class Beta(MongoDBModel):
            alpha = Field(belongs_to='Alpha')

        await Alpha.drop()
        await Beta.drop()

        alpha = Alpha()
        beta = Beta()

        await alpha.save()
        await beta.save()

        await alpha.beta.push(beta)

        betas = [ model.id async for model in alpha.beta.objects ]

        self.assertIn(beta.id, betas)

    async def test_has_many_pull(self):

        class Alpha(MongoDBModel):
            beta = Field(has_many='Beta')

        class Beta(MongoDBModel):
            alpha = Field(belongs_to='Alpha')

        await Alpha.drop()
        await Beta.drop()

        alpha = Alpha()
        beta = Beta()

        await alpha.save()
        await beta.save()

        await alpha.beta.push(beta)

        await alpha.beta.pull(beta)

        betas = [ model.id async for model in alpha.beta.objects ]

        self.assertEqual([ ], betas)

    async def test_has_many_pop(self):

        class Alpha(MongoDBModel):
            beta = Field(has_many='Beta')

        class Beta(MongoDBModel):
            alpha = Field(belongs_to='Alpha')

        await Alpha.drop()
        await Beta.drop()

        alpha = Alpha()
        beta = Beta()

        await alpha.save()
        await beta.save()

        await alpha.beta.push(beta)
        await alpha.beta.push(beta)

        await alpha.beta.pop()

        betas = [ model.id async for model in alpha.beta.objects ]

        self.assertEqual(len(betas), 1)

    async def test_has_many_set(self):

        class Alpha(MongoDBModel):
            beta = Field(has_many='Beta')

        class Beta(MongoDBModel):
            alpha = Field(belongs_to='Alpha')

        await Alpha.drop()
        await Beta.drop()

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

        betas = [ model.id async for model in alpha.beta.objects ]

        self.assertIn(beta1.id, betas)
        self.assertIn(beta2.id, betas)

    async def test_has_many_create(self):

        class Alpha(MongoDBModel):
            beta = Field(has_many='Beta')

        class Beta(MongoDBModel):
            alpha = Field(belongs_to='Alpha', auto_delete=True)

        await Alpha.drop()
        await Beta.drop()

        alpha = Alpha()

        await alpha.save()

        await alpha.beta.create()


        async for beta in alpha.beta.objects:
            self.assertEqual((await beta.alpha.object).id, alpha.id)

    async def test_has_many_delete(self):

        class Alpha(MongoDBModel):
            beta = Field(has_many='Beta')

        class Beta(MongoDBModel):
            alpha = Field(belongs_to='Alpha', auto_delete=True)

        await Alpha.drop()
        await Beta.drop()

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

    async def test_has_one_set(self):

        class Alpha(MongoDBModel):
            beta = Field(has_one='Beta')

        class Beta(MongoDBModel):
            alpha = Field(belongs_to='Alpha', auto_delete=True)

        await Alpha.drop()
        await Beta.drop()

        alpha = Alpha()
        beta = Beta()

        await alpha.save()
        await beta.save()

        alpha.beta = beta
        beta.alpha = alpha

        await alpha.save()
        await beta.save()

        self.assertEqual((await alpha.beta.object).id, beta.id)
        self.assertEqual((await beta.alpha.object).id, alpha.id)

    async def test_has_one_delete(self):

        class Alpha(MongoDBModel):
            beta = Field(has_one='Beta')

        class Beta(MongoDBModel):
            alpha = Field(belongs_to='Alpha', auto_delete=True)

        await Alpha.drop()
        await Beta.drop()

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
