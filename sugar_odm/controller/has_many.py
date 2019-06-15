from bson import ObjectId

from .. modelmeta import ModelMeta, get_class

from . controller import Controller


class HasMany(Controller):

    def __init__(self, *args, **kargs):
        super(HasMany, self).__init__(*args, **kargs)
        if not isinstance(self.model._data.get(self.field.name), list):
            self.model._data[self.field.name] = [ ]

    def _check(self, value):
        if isinstance(value, str):
            _ = ObjectId(value)
        elif isinstance(type(value), ModelMeta):
            if not value.id:
                raise Exception(f'{type(value)} has not been saved.')

    async def _set_related(self, model):
        for field in model._belongs_to:
            if get_class(field.belongs_to) == self.model.__class__:
                model.set(field.name, self.model.id)
        await model.save()

    @property
    async def objects(self):
        for id in self.model._data[self.field.name]:
            model = await get_class(self.field.has_many).find_one({
                get_class(self.field.has_many)._primary: ObjectId(id)
            })
            if not model:
                continue
            yield model

    async def create(self, *args, **kargs):
        model = get_class(self.field.has_many)(*args, **kargs)
        await self._set_related(model)
        await self.push(model.id)
        return model

    async def push(self, value):
        self._check(value)
        if isinstance(type(value), ModelMeta):
            await self._set_related(value)
            value = value.id
        await self.model.operation({
            '$push': { self.field.name: value }
        })

    async def pull(self, value):
        self._check(value)
        if isinstance(type(value), ModelMeta):
            _value = value
            value = value.id
            await _value.delete()
        await self.model.operation({
            '$pull': { self.field.name: value }
        })

    async def pop(self, index=1):
        await self.model.operation({
            '$pop': { self.field.name: index }
        })

    def check(self, iterable):
        for value in iterable:
            self._check(value)

    def _map(self, value):
        if isinstance(value, str):
            return value
        else:
            return value.id

    def set(self, iterable):
        self.check(iterable)
        self.model._data[self.field.name] = list(map(self._map, iterable))
