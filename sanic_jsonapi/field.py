
class Field(object):

    def __init__(self, type=str, primary=False, required=False, related=False, indexed=False, computed=False, computed_empty=False, computed_type=False):
        self.name = None
        self.type = type
        self.primary = primary
        self.required = required
        self.related = related
        self.indexed = indexed
        self.computed = computed
        self.computed_empty = computed_empty
        self.computed_type = computed_type

        self.parent = None

        if self.primary:
            if not self.type in (bool, int, float, str):
                raise AttributeError('The primary key for a field must be of type: (bool, int, float, str).')

    def __repr__(self):
        return '<Field name:{name}>'.format(name=self.name)

    def __str__(self):
        return repr(self)
