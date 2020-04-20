
class Field(object):
    '''
    The field object.

    :param type: The field type.
    :param primary: If the field is the primary key.
    :param required: If the field is required.
    :param validated: If the field is validated.
    :param computed: If the field is computed.
    :param computed_empty: Only computed the field when empty.
    :param computed_type: Do not convert to `type`, instead use the output of the computed function.
    :param has_one: The related `Model`.
    :param has_many: The related `Model`.
    :param belongs_to: The related `Model`.
    :param auto_delete: Whether or not to delete the `model` if the `model` it belongs to is deleted.
    :param validated_before_computed: Whether or not to validate the `field` before it is `computed`.
    :param default: Synonym for `computed`.
    :param default_empty: Synonym for `computed_empty`.
    :param default_type: Synonym for `computed_type`.
    '''

    def __init__(self, type=str, primary=False, required=False, validated=False, computed=False, computed_empty=False, computed_type=False, has_one=False, has_many=False, belongs_to=False, auto_delete=False, validated_before_computed=False, default=False, default_empty=False, default_type=False):
        self._controller = None
        self._model = None
        self.name = None
        self.type = type
        self.primary = primary
        self.required = required
        self.validated = validated
        self.validated_before_computed = validated_before_computed
        if default:
            self.computed = default
            self.computed_empty = default_empty
            self.computed_type = default_type
        else:
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
