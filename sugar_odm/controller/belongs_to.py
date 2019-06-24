from bson import ObjectId

from .. modelmeta import ModelMeta, get_class

from . controller import Controller



class BelongsTo(Controller):

    @property
    async def object(self):
        return await get_class(self.field.belongs_to).find_one({
            get_class(self.field.belongs_to)._primary: \
                ObjectId(self.model._data[self.field.name])
        })

    def check(self, value):
        if isinstance(value, str):
            _ = ObjectId(value)
        elif isinstance(type(value), ModelMeta):
            if not value.id:
                raise Exception(f'{type(value)} has not been saved.')

    def set(self, value):
        self.check(value)
        if isinstance(value, str):
            self.model._data[self.field.name] = value
        else:
            self.model._data[self.field.name] = value.id
