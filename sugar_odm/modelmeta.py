import inspect
import inflection

from . field import Field


__registry__ = { }

def register_class(name, cls):
    global __registry__
    __registry__[name] = cls

def get_class(name):
    global __registry__
    return __registry__[name]


class ModelMeta(type):

    def __init__(cls, name, bases, attrs):
        super(ModelMeta, cls).__init__(name, bases, attrs)

        # XXX: this should not be applied to Model
        register_class(cls.__name__, cls)

        cls._field = None

        cls._table = inflection.tableize(cls.__name__)

        cls._fields = [ ]
        cls._nested = [ ]
        cls._related = [ ]
        cls._required = [ ]
        cls._indexed = [ ]
        cls._validated = [ ]
        cls._computed = [ ]
        cls._dynamic = [ ]
        cls._list = [ ]
        cls._has_one = [ ]
        cls._has_many = [ ]
        cls._belongs_to = [ ]
        cls._auto_delete = [ ]

        members = inspect.getmembers(cls, lambda item: isinstance(item, Field))

        for name, field in members:

            field.name = name
            field._model = cls

            if inspect.isclass(field.type) \
                and isinstance(field.type, ModelMeta):
                field.type._field = field
                cls._nested.append(field)

            if isinstance(field.type, list):
                cls._list.append(field)
                for item in field.type:
                    if isinstance(item, ModelMeta):
                        item._field = field

            if isinstance(field.type, str) \
                or inspect.isfunction(field.type) \
                or inspect.ismethod(field.type):
                cls._dynamic.append(field)

            if field.required:
                cls._required.append(field)

            if field.indexed:
                cls._indexed.append(field)

            if field.validated:
                cls._validated.append(field)

            if field.computed:
                cls._computed.append(field)

            if field.has_one:
                cls._has_one.append(field)

            if field.has_many:
                field.type = list
                cls._has_many.append(field)

            if field.belongs_to:
                cls._belongs_to.append(field)

            if field.auto_delete:
                cls._auto_delete.append(field)

            cls._fields.append(field)

        cls._check_primary()

        cls._check_methods(cls._validated, 'validated')
        cls._check_methods(cls._computed, 'computed')
        cls._check_methods(cls._dynamic, 'type')

        cls._check_callable(cls._validated, 'validated')
        cls._check_callable(cls._computed, 'computed')
        cls._check_callable(cls._dynamic, 'type')

        cls.initialize()

    def initialize(cls):
        pass

    def default_primary(cls):
        pass

    def check_primary(cls, primary):
        pass

    def _check_primary(cls):
        primary = list(filter(lambda field: field.primary, cls._fields))

        if len(primary) > 1:
            fields = list(map(lambda field: field.name, primary))
            message = '{model} has multiple primary fields: {fields}'.format(
                model=cls.__name__,
                fields=','.join(fields)
            )
            raise AttributeError(message)

        if not primary:

            field = cls.default_primary()

            if field:
                cls._fields.append(field)
                primary.append(field)


        if len(primary) == 0:
            cls._primary = None
        else:
            cls.check_primary(primary[0])
            cls._primary = primary[0].name

    def _check_methods(cls, fields, attr):
        methods = list(filter(lambda field: \
            isinstance(getattr(field, attr), str), fields))

        missing = list(filter(lambda field: \
            not hasattr(cls, getattr(field, attr)), methods))

        if len(missing) > 0:
            names = list(map(lambda field: getattr(field, attr), missing))
            message = '{model} has missing methods: {methods}'.format(
                model=cls.__name__,
                methods=','.join(names)
            )
            raise AttributeError(message)

    def _check_callable(cls, fields, attr):
        methods = list(filter(lambda field: \
            isinstance(getattr(field, attr), str), fields))

        invalid_methods = list(filter(lambda field: \
            not callable(getattr(cls, getattr(field, attr))), methods))

        if len(invalid_methods) > 0:
            names = list(map(lambda field: \
                getattr(field, attr), invalid_methods))
            message = '{model} has non-callable bindings: {methods}'.format(
                model=cls.__name__,
                methods=','.join(names)
            )
            raise AttributeError(message)

        functions = list(filter(lambda field: \
            not isinstance(getattr(field, attr), str), fields))

        invalid_functions = list(filter(lambda field: \
            not callable(getattr(field, attr)), functions))

        if len(invalid_functions) > 0:
            names = list(map(lambda field: \
                field.name, invalid_functions))
            message = '{model} has non-callable bindings: {methods}'.format(
                model=cls.__name__,
                methods=','.join(names)
            )
            raise AttributeError(message)
