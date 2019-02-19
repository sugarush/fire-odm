from . base import Controller, ControllerError


class ListController(Controller):

    def __init__(self, model, field):
        super(ListController, self).__init__(model, field)

        self.types = set( )

        if isinstance(self.field.type, list):
            self.types = set(self.field.type)
            self.field.type = list

        self.reload()
        self.to_append = [ ]
        self.to_remove = [ ]
        self.to_remove_all = [ ]
        self.to_empty = False
        self.to_replace = False

    def __iter__(self):
        return iter(self.data)

    def _check_operation(self):
        if self.to_empty or self.to_replace:
            raise ControllerError('The controller is set to empty or to replace the list. Please call "reset" first.')

    def _check_value(self, value):
        if self.types:
            if not type(value) in self.types:
                raise ControllerError('Invalid value type.')

    def _check_values(self, values):
        for value in values:
            self._check_value(value)

    def check(self, iterable):
        self._check_values(iterable)

    def serialize(self, reset=False):
        if self.to_empty:
            if reset: self.reset()
            return [ ]

        if self.to_replace:
            if reset: self.reset()
            return self.data

        data = self.data.copy()

        for item in self.to_remove_all:
            while item in data:
                data.remove(item)

        for item in self.to_remove:
            data.remove(item)

        for item in self.to_append:
            data.append(item)

        if reset:
            self.reset()

        return data

    def operations(self, reset=False):
        data = { }

        if self.to_empty:
            data['$:list:empty'] = self.to_empty
            if reset: self.reset()
            return data

        if self.to_replace:
            data['$:list:replace'] = self.data.copy()
            if reset: self.reset()
            return data

        if self.to_append:
            data['$:list:append'] = self.to_append.copy()

        if self.to_remove:
            data['$:list:remove'] = self.to_remove.copy()

        if self.to_remove_all:
            data['$:list:remove_all'] = self.to_remove_all.copy()

        if reset:
            self.reset()

        return data

    def set(self, iterable):
        self._check_values(iterable)
        self.reset()
        if len(self.data) > 0:
            self.to_replace = True
        self.data = self.field.type(iterable)

    def reload(self):
        self.data = self.model.get_direct(self.field.name, [ ]).copy()

    def append(self, value):
        self._check_operation()
        self._check_value(value)
        self.to_append.append(value)

    def remove(self, value):
        self._check_operation()
        self._check_value(value)
        self.to_remove.append(value)

    def remove_all(self, value):
        self._check_operation()
        self._check_value(value)
        self.to_remove_all.append(value)

    def reset(self):
        self.reload()
        self.to_append.clear()
        self.to_remove.clear()
        self.to_remove_all.clear()
        self.to_empty = False
        self.to_replace = False

    def empty(self):
        self.reset()
        self.to_empty = True
