from unittest import skip

from sugar_asynctest import AsyncTestCase

from sugar_odm import MongoDBModel, Model, Field
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

    async def test_has_one_create(self):

        class Alpha(MongoDBModel):
            beta = Field(has_one='Beta')

        class Beta(MongoDBModel):
            alpha = Field(belongs_to='Alpha', auto_delete=True)

        await Alpha.drop()
        await Beta.drop()

        alpha = Alpha()

        await alpha.save()

        beta = await alpha.beta.create()

        await alpha.save()

        self.assertEqual((await alpha.beta.object).id, beta.id)

    async def test_has_one_create_delete(self):

        class Alpha(MongoDBModel):
            beta = Field(has_one='Beta')

        class Beta(MongoDBModel):
            alpha = Field(belongs_to='Alpha', auto_delete=True)

        await Alpha.drop()
        await Beta.drop()

        alpha = Alpha()

        await alpha.save()

        beta1 = await alpha.beta.create()
        beta2 = await alpha.beta.create()

        self.assertFalse(await Beta.exists(beta1.id))
        self.assertEqual((await alpha.beta.object).id, beta2.id)

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

    def test_get_root(self):

        class Beta(Model):
            field = Field()

        class Alpha(MongoDBModel):
            betas = Field(type=[ Beta ])

        alpha = Alpha({
            'betas': [
                Beta({ })
            ]
        })

        model, path = alpha.betas._get_root()

        self.assertEqual(model, alpha)
        self.assertEqual(path, 'betas')

    def test_get_root_nested(self):

        class Gamma(Model):
            field = Field()

        class Beta(Model):
            gammas = Field(type=[ Gamma ])

        class Alpha(MongoDBModel):
            beta = Field(type=Beta)

        alpha = Alpha({
            'beta': {
                'gammas': [
                    Gamma({ })
                ]
            }
        })

        model, path = alpha.beta.gammas._get_root()

        self.assertEqual(model, alpha)
        self.assertEqual(path, 'beta.gammas')

    def test_get_root_nested_list(self):

        class Gamma(Model):
            field = Field()

        class Beta(Model):
            gammas = Field(type=[ Gamma ])

        class Alpha(MongoDBModel):
            betas = Field(type=[ Beta ])

        alpha = Alpha({
            'betas': [
                Beta({
                    'gammas': [
                        Gamma({ })
                    ]
                })
            ]
        })

        model, path = alpha.betas[0].gammas._get_root()

        self.assertEqual(model, alpha)
        self.assertEqual(path, 'betas.0.gammas')

    def test_list_nested_object(self):

        class Gamma(Model):
            field = Field()

        class Beta(Model):
            gammas = Field(type=[ Gamma ])

        class Alpha(MongoDBModel):
            betas = Field(type=[ Beta ])

        alpha = Alpha({
            'betas': [
                {
                    'gammas': [
                        { 'field': 'value' }
                    ]
                }
            ]
        })

        self.assertEqual(alpha.betas[0].gammas[0].field, 'value')
