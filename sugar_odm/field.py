
class Field(object):

    def __init__(self, type=str, primary=False, required=False, related=False, indexed=False, validated=False, computed=False, computed_empty=False, computed_type=False):
        self.name = None
        self.type = type
        self.primary = primary
        self.required = required
        self.indexed = indexed
        self.validated = validated
        self.computed = computed
        self.computed_empty = computed_empty
        self.computed_type = computed_type

    def __repr__(self):
        return f'<Field name:{self.name}>'

    def __str__(self):
        return repr(self)
