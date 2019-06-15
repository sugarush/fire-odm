from bson import ObjectId

from .. modelmeta import ModelMeta, get_class

from . controller import Controller


class HasOne(Controller):

    @property
    async def object(self):
        return await get_class(self.field.has_one).find_one({
            get_class(self.field.has_one)._primary: \
                ObjectId(self.model._data[self.field.name])
        })

    async def create(self, *args, **kargs):
        model = get_class(self.field.has_one)(*args, **kargs)
        for field in model._belongs_to:
            if get_class(field.belongs_to) == self.model.__class__:
                model.set(field.name, self.model.id)
        await model.save()
        old_id = self.model._data.get(self.field.name)
        if old_id and await get_class(self.field.has_one).exists(old_id):
            old_model = await get_class(self.field.has_one).find_one({
                get_class(self.field.has_one)._primary: ObjectId(old_id)
            })
            await old_model.delete()
        self.set(model)
        return model

    def check(self, value):
        if isinstance(value, str):
            _ = ObjectId(value)
        elif isinstance(type(value), ModelMeta):
            if not value.id:
                raise Exception(f'{type(value)} has not been saved.')

    def set(self, value):
        self.check(value)
        self._value = value
        if isinstance(value, str):
            self.model._data[self.field.name] = value
        else:
            self.model._data[self.field.name] = value.id
