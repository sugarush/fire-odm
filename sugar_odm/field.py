
class Field(object):

    def __init__(self, type=str, primary=False, required=False, related=False, validated=False, computed=False, computed_empty=False, computed_type=False, has_one=False, has_many=False, belongs_to=False, auto_delete=False, validated_before_computue=False):
        self._controller = None
        self._model = None
        self.name = None
        self.type = type
        self.primary = primary
        self.required = required
        self.validated = validated
        self.validated_before_computue = validated_before_computue
        self.computed = computed
        self.computed_empty = computed_empty
        self.computed_type = computed_type
        self.has_one = has_one
        self.has_many = has_many
        self.belongs_to = belongs_to
        self.auto_delete = auto_delete

    def __repr__(self):
        return f'<Field name:{self.name}>'

    def __str__(self):
        return repr(self)
