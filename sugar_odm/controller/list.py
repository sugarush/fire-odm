from .. modelmeta import ModelMeta

from . controller import Controller


class List(Controller):

    def __init__(self, *args, **kargs):
        super(List, self).__init__(*args, **kargs)
        self._types = [ ]
        self._index = None

        if isinstance(self.field.type, list):
            if not len(self.field.type) >= 1:
                raise Exception('List fields can have no type, or one type.')
            self._types = list(self.field.type)

    def _check(self, value):
        if self._types:
            if type(value) == dict and len(self._types) == 1:
                self._types[0](value)
            elif not type(value) in self._types:
                raise Exception(f'{type(value)} not in {self._types}.')

    def check(self, iterable):
        if self._types:
            for value in iterable:
                self._check(value)

    def serialize(self):
        obj = self.model._data[self.field.name].copy()
        for i in range(len(obj)):
            if isinstance(type(obj[i]), ModelMeta):
                obj[i] = obj[i].serialize()
        return obj

    def set(self, iterable):
        self.check(iterable)
        data = [ ]
        for item in iterable:
            if self._types:
                if isinstance(self._types[0], ModelMeta):
                    if isinstance(type(item), ModelMeta):
                        item._parent_model = self.model
                        item._parent_field_name = self.field.name
                        data.append(item)
                    elif isinstance(item, dict):
                        model = self._types[0](item)
                        model._parent_model = self.model
                        model._parent_field_name = self.field.name
                        data.append(model)
                else:
                    value = this._types[0](item)
                    data.append(value)
            else:
                data.append(item)
        self.model._data[self.field.name] = data

        if len(self._types) == 1 \
            and isinstance(self._types[0], ModelMeta):
            for model in iterable:
                if not isinstance(type(model), ModelMeta):
                    model = self._types[0](model)
                model._parent_model = self.model
                model._parent_field_name = self.field.name
                data.append(model)
        self.model._data[self.field.name] = data

    def __getitem__(self, index):
        if not index >= 0:
            raise Exception('List indices must be positive.')
        self._index = str(index)
        return self.model._data[self.field.name][index]

    def _get_root(self):
        root = self.model
        path = [ self.field.name ]
        while root._parent_model:
            controller = \
                root._parent_model._get_controller(root._parent_field_name)
            if controller and controller._index:
                path.insert(0, controller._index)
                controller._index = None
            path.insert(0, root._parent_field_name)
            root = root._parent_model
        return (root, '.'.join(path))

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
                if not len(self._types) == 1:
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
