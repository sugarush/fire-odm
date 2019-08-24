from . controller import Controller


class List(Controller):

    def __init__(self, *args, **kargs):
        super(List, self).__init__(*args, **kargs)
        self.types = None
        if isinstance(self.field.type, list):
            self.types = set(self.field.type)

    def __getitem__(self, index):
        return self.model._data[self.field.name][index]

    def _get_root(self):
        field = self.field
        path = [ field.name ]
        root = None
        while field._model:
            root = field._model
            if not field._model._field:
                break
            field = field._model._field
            path.insert(0, field.name)
        return (root, '.'.join(path))

    def _check(self, value):
        if self.types:
            if not type(value) in self.types:
                raise Exception(f'{type(value)} not in {self.types}.')

    def check(self, iterable):
        if self.types:
            for value in iterable:
                self._check(value)

    def set(self, iterable):
        self.check(iterable)
        self.model._data[self.field.name] = list(iterable)

    def append(self, value):
        pass

    def pop(self, index=-1):
        pass

    async def push(self, value, type=None):
        if type:
            # XXX: we need to check that type is either the same as
            # XXX: self.field.type or that type is in self.field.type
            # XXX: if it is a list.
            pass
        else:
            if isinstance(self.field.type, list):
                if not len(self.field.type) == 1:
                    raise Exception(
                        f'Cannot determine type of field {self.field.name}.'
                    )
                type = self.field.type[0]
            type = self.field.type
        model, path = self._get_root()
        await model.operation({
            '$push': { path: type(value) }
        })
        await root.load()

    async def pull(self, value):
        model, path = self._get_root()
        await model.operation({
            '$pull': { path: value }
        })
        await root.load()
