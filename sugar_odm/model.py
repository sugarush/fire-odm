import json
import inspect

from . modelmeta import ModelMeta
from . field import Field

from . controller.list import ListController


class Model(object, metaclass=ModelMeta):

    @classmethod
    async def drop(cls):
        raise NotImplementedError('Model.drop not implemented.')

    @classmethod
    async def exists(cls, id):
        raise NotImplementedError('Model.exists not implemented.')

    @classmethod
    async def find_one(cls, id):
        raise NotImplementedError('Model.find_one not implemented.')

    @classmethod
    async def find(cls, query={ }):
        raise NotImplementedError('Model.find not implemented.')

    @classmethod
    async def add(cls, *args):
        raise NotImplementedError('Model.add not implemented.')

    async def save(self):
        raise NotImplementedError('Model.save not implemented.')

    async def load(self):
        raise NotImplementedError('Model.load not implemented.')

    async def delete(self):
        raise NotImplementedError('Model.delete not implemented.')

    def __init__(self, dictionary=None, **kargs):
        self._data = { }
        self._controllers = { }
        self._create_controllers()
        self.update_direct(dictionary, **kargs)

    def __repr__(self):
        return json.dumps(self.serialize(controllers=True),
            indent=4, sort_keys=True)

    def __str__(self):
        return repr(self)

    def __getattribute__(self, name):
        attr = super(Model, self).__getattribute__(name)
        if type(attr) == Field:
            return self.get(name)
        return attr

    def __setattr__(self, name, value):
        if not name == self._primary and self._get_field(name):
            self.set(name, value)
        else:
            super(Model, self).__setattr__(name, value)

    def __getitem__(self, name):
        return self.get(name)

    def __setitem__(self, name, value):
        self.set(name, value)

    @property
    def id(self):
        if self._primary:
            return self.get(self._primary)
        else:
            message = "Cannot get \"id\" because model {model} has no primary key.".format(
                model=self.__class__.__name__
            )
            raise Exception(message)

    @id.setter
    def id(self, value):
        if self._primary:
            self.set(self._primary, value)
        else:
            message = "Cannot set \"id\" because model {model} has no primary key.".format(
                model=self.__class__.__name__
            )
            raise Exception(message)

    @classmethod
    def _check_undefined(cls, kargs):
        undefined = list(filter(lambda karg: \
            karg not in map(lambda field: field.name, cls._fields), kargs))

        if len(undefined) > 0:
            message = '{model} has undefined fields: {fields}'.format(
                model=cls.__name__,
                fields=','.join(undefined)
            )
            raise Exception(message)

    @classmethod
    def _check_missing(cls, kargs):
        missing = list(map(lambda field: field.name, \
            filter(lambda field: field.name not in kargs, \
            cls._required)))

        if len(missing) > 0:
            message = '{model} has missing fields: {fields}'.format(
                model=cls.__name__,
                fields=','.join(missing)
            )
            raise Exception(message)

    @classmethod
    def _check_field(cls, key):
        field = cls._get_field(key)

        if not field:
            message = '{model} does not have field: {field}'.format(
                model=cls.__name__,
                field=key
            )
            raise Exception(message)

        return field

    @classmethod
    def _get_field(cls, key):
        field = list(filter(lambda field: field.name == key, cls._fields))
        if field:
            return field[0]
        return None

    def _create_controllers(self):
        for field in self._fields:
            if field.type == list or isinstance(field.type, list):
                self._controllers[field.name] = ListController(self, field)

    def _get_controller(self, key):
        return self._controllers.get(key)

    def set(self, key, value, direct=False):
        field = self._check_field(key)
        controller = self._get_controller(field.name)

        # field has a controller
        if controller:
            if direct:
                controller.check(value)
                self._data[key] = field.type(value)
                controller.reload()
            else:
                controller.set(value)
        # field's type is a string for a method on this object
        elif isinstance(field.type, str):
            self._data[key] = getattr(self, field.type)(value)
        # field's type is a type, method or function
        elif type(field.type) == type \
            or inspect.isfunction(field.type) \
            or inspect.ismethod(field.type):
            self._data[key] = field.type(value)
        # field's type is a nested model
        elif inspect.isclass(field.type) \
            and issubclass(field.type, Model):
            if isinstance(value, field.type):
                self._data[key] = field.type(value._data)
            elif isinstance(value, dict):
                self._data[key] = field.type(value)
            else:
                message = '{model}\'s field "{field}" must be set with a dict or {type} object.'.format(
                    model=self.__class__.__name__,
                    field=field.name,
                    type=field.type.__name__
                )
                raise Exception(message)
        else:
            raise Exception('Model field error.')

    def get(self, key, default=None, direct=False):
        field = self._check_field(key)
        controller = self._get_controller(field.name)
        if controller and not direct:
            return controller
        return self._data.get(key, default)

    def update(self, dictionary=None, **kargs):
        if not dictionary:
            dictionary = { }

        dictionary.update(kargs)
        kargs = dictionary

        self._check_undefined(kargs)

        for karg in kargs:
            self.set(karg, kargs[karg])

    def set_direct(self, key, value):
        self.set(key, value, direct=True)

    def get_direct(self, key, default=None):
        return self.get(key, default, direct=True)

    def update_direct(self, dictionary=None, **kargs):
        if not dictionary:
            dictionary = { }

        dictionary.update(kargs)
        kargs = dictionary

        self._check_undefined(kargs)

        for karg in kargs:
            self.set_direct(karg, kargs[karg])

    def validate(self):
        self._check_missing(self._data)

        for field in self._fields:
            if inspect.isclass(field.type) \
                and issubclass(field.type, Model):
                # verify that nested models have required fields
                model = self._data.get(field.name, field.type())
                model.validate()
            elif field.validated:
                controller = self._get_controller(field.name)
                if controller:
                    if isinstance(field.validated, str):
                        getattr(self, field.validated)(controller.serialize())
                    else: # field.validated is not a string
                        field.validated(controller.serialize())
                elif field.computed:
                    value = self.get(field.name)
                    if field.computed_type:
                        if field.computed_empty and value:
                            if isinstance(field.validated, str):
                                getattr(self, field.validated)(value)
                            else: # field.validated is not a string
                                field.validated(value)
                        else: # field.computed_empty is false or no value
                            if isinstance(field.computed, str):
                                if isinstance(field.validated, str):
                                    value = getattr(self, field.computed)()
                                    getattr(self, field.validated)(value)
                                else: # field.validated is not a string
                                    value = getattr(self, field.computed)()
                                    field.validated(value)
                            else: # field.computed is not a string
                                if isinstance(field.validated, str):
                                    value = field.computed()
                                    getattr(self, field.validated)(value)
                                else: # field.validated is not a string
                                    value = field.computed()
                                    field.validated(value)
                    else: # field.computed_type is false
                        if field.computed_empty and value:
                            # XXX: calls to field.type may not be necessary in
                            # XXX: this block. value is typed when it is set on
                            # XXX: this object.
                            if isinstance(field.validated, str):
                                value = field.type(value)
                                getattr(self, field.validated)(value)
                            else: # field.validated is not a string
                                value = field.type(value)
                                field.validated(value)
                        else: # field.computed_empty is false or no value
                            if isinstance(field.validated, str):
                                if isinstance(field.computed, str):
                                    value = getattr(self, field.computed)()
                                    value = field.type(value)
                                    getattr(self, field.validated)(value)
                                else: # field.computed is not a string
                                    value = field.computed()
                                    value = field.type(value)
                                    getattr(self, field.validated)(value)
                            else: # field.validated is not a string
                                if isinstance(field.computed, str):
                                    value = getattr(self, field.computed)()
                                    value = field.type(value)
                                    field.validated(value)
                                else: # field.computed is not a string
                                    value = field.computed()
                                    value = field.type(value)
                                    field.validated(value)
                else: # field.computed is not a truthy value
                    # XXX: calls to field.type may not be necessary in
                    # XXX: this block. value is typed when it is set on
                    # XXX: this object.
                    value = self.get(field.name)
                    if value:
                        if isinstance(field.validated, str):
                            value = field.type(value)
                            getattr(self, field.validated)(value)
                        else:
                            value = field.type(value)
                            field.validated(value)

    def serialize(self, computed=False, controllers=False, reset=False):
        obj = self._data.copy()

        for field in self._fields:
            controller = self._get_controller(field.name)
            if controllers and controller:
                obj[field.name] = controller.serialize(reset=reset)
            elif inspect.isclass(field.type) \
                and issubclass(field.type, Model):
                model = self.get_direct(field.name, field.type())
                data = model.serialize(
                    computed=computed,
                    controllers=controllers,
                    reset=reset
                )
                if data: obj[field.name] = data
            elif computed and field.computed:
                if field.computed_empty \
                    and obj.get(field.name):
                    # skip fields that should only be computed when empty
                    continue
                elif field.computed_type:
                    if type(field.computed) == str:
                        value = getattr(self, field.computed)()
                        obj[field.name] = value
                    else:
                        value = field.computed()
                        obj[field.name] = value
                else:
                    if type(field.computed) == str:
                        value = field.type(getattr(self, field.computed)())
                        obj[field.name] = value
                    else:
                        value = field.type(field.computed())
                        obj[field.name] = value

        return obj

    def operations(self, reset=False):
        data = { }

        for field in self._fields:
            controller = self._get_controller(field.name)
            if controller:
                data[field.name] = controller.operations(reset=reset)
            elif inspect.isclass(field.type) \
                and issubclass(field.type, Model):
                model = self.get_direct(field.name, field.type())
                data[field.name] = model.operations(reset=reset)

        return data
