import json
import inspect

from . modelmeta import ModelMeta
from . field import Field

from . controller.list import ListController


class Model(object, metaclass=ModelMeta):

    def __init__(self, dictionary=None, **kargs):
        self._data = { }
        self._controllers = { }
        self._create_controllers()
        self.update_direct(dictionary, **kargs)

    def __repr__(self):
        return json.dumps(self.serialize(controllers=True), indent=4)

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
        pass

    def __setitem__(self, name, value):
        pass

    @property
    def id(self):
        return self.get(self._primary)

    @id.setter
    def id(self, value):
        self.set(self._primary, value)

    @classmethod
    def _check_undefined(cls, kargs):
        undefined = list(filter(lambda karg: \
            karg not in map(lambda field: field.name, cls._fields), kargs))

        if len(undefined) > 0:
            message = '{model} has undefined fields: {fields}'.format(
                model=cls.__name__,
                fields=','.join(undefined)
            )
            raise Error(
                title = 'Model Field Error',
                detail = message
            )

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
            raise Error(
                title = 'Model Field Error',
                detail = message
            )

    @classmethod
    def _check_field(cls, key):
        field = cls._get_field(key)

        if not field:
            message = '{model} does not have field: {field}'.format(
                model=cls.__name__,
                field=key
            )
            raise Error(
                title = 'Model Field Error',
                detail = message
            )

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
            try:
                if direct:
                    controller.check(value)
                    self._data[key] = field.type(value)
                    controller.reload()
                else:
                    controller.set(value)
            except Exception as error:
                raise Error(
                    title = 'Type Conversion Error',
                    detail = str(error)
                )
        # field's type is a string for a method on this object
        elif isinstance(field.type, str):
            try:
                self._data[key] = getattr(self, field.type)(value)
            except Exception as error:
                raise Error(
                    title = 'Type Conversion Error',
                    detail = str(error)
                )
        # field's type is a type, method or function
        elif type(field.type) == type \
            or inspect.isfunction(field.type) \
            or inspect.ismethod(field.type):
            try:
                self._data[key] = field.type(value)
            except ValueError as error:
                raise Error(
                    title = 'Type Conversion Error',
                    detail = str(error)
                )
        # field's type is a nested model
        elif inspect.isclass(field.type) \
            and issubclass(field.type, Model):
            if isinstance(value, field.type):
                self._data[key] = field.type(value._data)
            elif isinstance(value, dict):
                self._data[key] = field.type(value)
            else:
                raise Error(
                    title = 'Model Field Error',
                    detail = '{model}\'s field "{field}" must be set with a dict or {type} object.'.format(
                        model=self.__class__.__name__,
                        field=field.name,
                        type=field.type.__name__
                    )
                )
        else:
            raise Error(
                title = 'Model Field Error'
            )

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
                        obj[field.name] = getattr(self, field.computed)()
                    else:
                        obj[field.name] = field.computed()
                else:
                    if type(field.computed) == str:
                        obj[field.name] = field.type(getattr(self, field.computed)())
                    else:
                        obj[field.name] = field.type(field.computed())

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

    @classmethod
    async def exists(cls, id):
        raise NotImplementedError()

    @classmethod
    async def find_one(cls, id):
        raise NotImplementedError()

    @classmethod
    async def find(cls, query={ }):
        raise NotImplementedError()

    @classmethod
    async def add(cls, *args):
        raise NotImplementedError()

    async def save(self):
        raise NotImplementedError()

    async def load(self):
        raise NotImplementedError()

    async def delete(self):
        raise NotImplementedError()


class Links(Model):
    about = Field()


class Source(Model):
    pointer = Field()
    parameter = Field()


class Error(Model, Exception):
    id = Field()
    links = Field(type=Links)
    status = Field(type=int)
    code = Field()
    title = Field()
    detail = Field()
    source = Field(type=Source)
    meta = Field(type=dict)
