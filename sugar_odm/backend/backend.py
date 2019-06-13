

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
