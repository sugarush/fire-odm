from bson import ObjectId

from .. modelmeta import ModelMeta

from . controller import Controller


class HasMany(Controller):

    def __init__(self, *args, **kargs):
        super(HasMany, self).__init__(*args, **kargs)
        if not isinstance(self.model._data.get(self.field.name), list):
            self.model._data[self.field.name] = [ ]

    @property
    async def objects(self):
        for id in self.model._data[self.field.name]:
            model = await self.field.has_many.find_one({
                self.field.has_many._primary: ObjectId(id)
            })
            if not model:
                continue
            yield model

    async def push(self, value):
        self._check(value)
        if isinstance(type(value), ModelMeta):
            value = value.id
        await self.model.operation({
            '$push': { self.field.name: value }
        })

    async def pull(self, value):
        self._check(value)
        if isinstance(type(value), ModelMeta):
            value = value.id
        await self.model.operation({
            '$pull': { self.field.name: value }
        })

    def _check(self, value):
        if isinstance(value, str):
            _ = ObjectId(value)
        elif isinstance(type(value), ModelMeta):
            if not value.id:
                raise Exception(f'{type(value)} has not been saved.')

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
