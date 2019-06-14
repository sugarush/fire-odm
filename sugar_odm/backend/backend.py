

class RelationshipMixin(object):

    async def delete_related(self):

        for field in self._has_one:
            for related_field in field.has_one._belongs_to:
                if related_field.belongs_to == self.__class__ \
                    and related_field.auto_delete:
                    model = await field.has_one.find_one({
                        related_field.name: self.id
                    })
                    await model.delete()

        for field in self._has_many:
            for related_field in field.has_many._belongs_to:
                if related_field.belongs_to == self.__class__ \
                    and related_field.auto_delete:
                    models = field.has_many.find({
                        related_field.name: self.id
                    })
                    async for model in models:
                        await model.delete()

        for field in self._belongs_to:

            for related_field in field.belongs_to._has_one:
                if related_field.has_one == self.__class__:
                    model = await field.belongs_to.find_one({
                        related_field.name: self.id
                    })
                    if model:
                        model.set_direct(related_field.name, None)
                        await model.save()

            for related_field in field.belongs_to._has_many:
                if related_field.has_many == self.__class__:
                    models = field.belongs_to.find({
                        related_field.name: {
                            '$all': [ self.id ]
                        }
                    })
                    async for model in models:
                        print(related_field.name, self.id)
                        await model.operation({
                            '$pull': {
                                related_field.name: self.id
                            }
                        })
                        await model.load()
