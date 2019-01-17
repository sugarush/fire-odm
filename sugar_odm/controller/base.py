import json
from abc import ABC, abstractmethod


class ControllerError(Exception):
    pass


class Controller(ABC):

    def __init__(self, model, field):
        self.model = model
        self.field = field

    def __repr__(self):
        return json.dumps(self.serialize(), indent=4, sort_keys=True)

    def __str__(self):
        return repr(self)

    @abstractmethod
    def check(self, value):
        pass

    @abstractmethod
    def serialize(self):
        pass

    @abstractmethod
    def operations(self):
        pass

    @abstractmethod
    def set(self, value):
        pass

    @abstractmethod
    def reload(self):
        pass
