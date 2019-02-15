from uuid import uuid4

from .. model import Model, Field


def find(db, query={ }):
    for _, data in db.items():

        def match(item):
            _data = data
            path = item[0]
            value = item[1]
            for key in path.split('.'):
                _data = _data.get(key)
                if not _data:
                    return False
            if not _data == value:
                return False
            return True

        if all(map(match, query.items())):
            yield data


class MemoryModel(Model):

    @classmethod
    def initialize(cls):
        cls.db = { }

    @classmethod
    def default_primary(cls):
        field = Field()
        field.name = 'id'
        field.type = str
        return field

    @classmethod
    async def count(cls):
        return len(cls.db)

    @classmethod
    async def drop(cls):
        for id in cls.db.copy():
            del cls.db[id]

    @classmethod
    async def exists(cls, id):
        if id in cls.db:
            return True
        return False

    @classmethod
    async def find_by_id(cls, id):
        data = cls.db.get(id)
        if data:
            return cls(data)
        return None

    @classmethod
    async def find_one(cls, query={ }):
        for data in find(cls.db, query):
            return cls(data)
        return None

    @classmethod
    async def find(cls, query={ }):
        for data in find(cls.db, query):
            yield cls(data)

    @classmethod
    async def add(cls, args):
        if isinstance(args, dict):
            model = cls(args)
            await model.save()
            return model
        elif isinstance(args, list):
            models = [ ]
            for data in args:
                model = cls(data)
                await model.save()
                models.append(model)
            return models
        else:
            message = 'Invalid argument to MemoryModel.add: must be a list or dict.'
            raise Exception(message)

    async def save(self):
        self.validate()
        if self.id:
            data = self.serialize(computed=True, controllers=True, reset=True)
            self.update_direct(data)
            self.db[self.id] = data
        else:
            self.id = uuid4()
            data = self.serialize(computed=True, controllers=True, reset=True)
            self.update_direct(data)
            self.db[self.id] = data

    async def load(self):
        if self.id:
            data = self.db.get(self.id)
            if data:
                self.update(data)
            else:
                message = 'No document for ID: {id}'.format(id=self.id)
                raise Exception(message)
        else:
            message = 'No document ID, cannot load.'
            raise Exception(message)

    async def delete(self):
        if self.id:
            if self.id in self.db:
                del self.db[self.id]
                self._data = { }
            else:
                message = 'No document for ID: {id}'.format(id=self.id)
                raise Exception(message)
        else:
            message = 'No document ID, cannot delete.'
            raise Exception(message)
