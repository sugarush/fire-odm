import inspect
import inflection

from . field import Field

class ModelMeta(type):

    def __init__(cls, name, bases, attrs):
        super(ModelMeta, cls).__init__(name, bases, attrs)

        cls._table = inflection.tableize(cls.__name__)
        #cls._route = '/' + cls._table

        cls._fields = [ ]
        cls._nested = [ ]
        cls._related = [ ]
        cls._required = [ ]
        cls._indexed = [ ]
        cls._computed = [ ]
        cls._dynamic = [ ]

        members = inspect.getmembers(cls, lambda f: isinstance(f, Field))

        for name, field in members:

            field.parent = cls
            field.name = name

            if inspect.isclass(field.type) \
                and isinstance(field.type, ModelMeta):
                if field.related:
                    cls._related.append(field)
                else:
                    cls._nested.append(field)

            if field.required:
                cls._required.append(field)

            if field.indexed:
                cls._indexed.append(field)

            if field.computed:
                cls._computed.append(field)

            if isinstance(field.type, str) \
                or inspect.isfunction(field.type) \
                or inspect.ismethod(field.type):
                cls._dynamic.append(field)

            cls._fields.append(field)

        cls._check_primary()
        cls._check_computed()
        cls._check_dynamic()

    def default_primary(cls):
        field = Field()
        field.name = 'id'
        return field

    def check_primary(cls, primary):
        if not primary.type in (bool, int, float, str):
            raise AttributeError('The primary key for a field must be of type: (bool, int, float, str).')

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
            field.primary = True
            cls._fields.append(field)
            primary.append(field)

        cls.check_primary(primary[0])

        cls._primary = primary[0].name

    def _check_computed(cls):
        methods = list(filter(lambda field: \
            isinstance(field.computed, str), cls._computed))

        missing = list(filter(lambda field: \
            not hasattr(cls, field.computed), methods))

        if len(missing) > 0:
            names = list(map(lambda field: field.computed, missing))
            message = '{model} has missing methods: {fields}'.format(
                model=cls.__name__,
                fields=','.join(names)
            )
            raise AttributeError(message)

    def _check_dynamic(cls):
        methods = list(filter(lambda field: \
            isinstance(field.type, str), cls._dynamic))

        missing = list(filter(lambda field: \
            not hasattr(cls, field.type), methods))

        if len(missing) > 0:
            names = list(map(lambda field: field.type, missing))
            message = '{model} has missing methods: {fields}'.format(
                model=cls.__name__,
                fields=','.join(names)
            )
            raise AttributeError(message)
