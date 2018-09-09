import json
import inspect

from . modelmeta import ModelMeta
from . field import Field


class Model(object, metaclass=ModelMeta):

    def __init__(self, dictionary=None, **kargs):
        self.set(dictionary, **kargs)

    def __repr__(self):
        return json.dumps(self.serialize(), indent=4)

    def __str__(self):
        return repr(self)

    def __getattribute__(self, name):
        attr = super(Model, self).__getattribute__(name)
        if type(attr) == Field:
            # XXX: evaluated only if the 'name' doesn't exist in self.__dict__
            # XXX: meaning the field is empty, so return None
            # return self.get(name) # XXX: may be used in the future
            return None
        return attr

    def __setattr__(self, name, value):
        attr = super(Model, self).__getattribute__(name)
        if type(attr) == Field:
            self._set(name, value)
        else:
            super(Model, self).__setattr__(name, value)

    @property
    def id(self):
        return self.get(self._primary)

    @id.setter
    def id(self, value):
        self._set(self._primary, value)

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
        field = list(filter(lambda field: field.name == key, cls._fields))

        if not field:
            message = '{model} does not have field: {field}'.format(
                model=cls.__name__,
                field=key
            )
            raise Error(
                title = 'Model Field Error',
                detail = message
            )

        return field[0]

    def _set(self, key, value):
        field = self._check_field(key)
        if type(field.type) == type or inspect.isfunction(field.type) or inspect.ismethod(field.type):
            try:
                self.__dict__[key] = field.type(value)
            except ValueError as error:
                raise Error(
                    title = 'Type Conversion Error',
                    detail = '{value_type} cannot be converted to {destination_type}'.format(
                        value_type = value.__class__.__name__,
                        destination_type = field.type.__name__
                    )
                )
        elif inspect.isclass(field.type) and issubclass(field.type, Model):
            if isinstance(value, field.type):
                self.__dict__[key] = field.type(value.__dict__)
            elif isinstance(value, dict):
                self.__dict__[key] = field.type(value)
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

    def set(self, _dictionary=None, **kargs):
        if not _dictionary:
            _dictionary = { }

        _dictionary.update(kargs)
        kargs = _dictionary

        self._check_undefined(kargs)

        for karg in kargs:
            self._set(karg, kargs[karg])

    def get(self, key, default=None):
        self._check_field(key)
        return self.__dict__.get(key, default)

    def validate(self):
        self._check_missing(self.__dict__)
        for field in self._fields:
            if inspect.isclass(field.type) and issubclass(field.type, Model):
                # XXX: check if nested models have required fields.
                model = self.__dict__.get(field.name, field.type())
                model.validate()

    def serialize(self, validate=False, compute=False):
        if validate:
            self.validate()

        obj = self.__dict__.copy()

        for field in self._fields:
            if inspect.isclass(field.type) and issubclass(field.type, Model):
                model = self.__dict__.get(field.name, field.type())
                # no need to pass validate to serialize here,
                # the call to self.validate() above is recursive
                data = model.serialize(compute=compute)
                if data: obj[field.name] = data
            elif compute and field.computed:
                if field.computed_empty and obj.get(field.name):
                    continue
                elif field.computed_type:
                    if type(field.computed) == str:
                        obj[field.name] = getattr(self, field.computed)()
                    else:
                        obj[field.name] = field.computed()
                    #obj[field.name] = field.computed()
                else:
                    if type(field.computed) == str:
                        obj[field.name] = field.type(getattr(self, field.computed)())
                    else:
                        obj[field.name] = field.type(field.computed())
                    #obj[field.name] = field.type(field.computed())

        return obj

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
