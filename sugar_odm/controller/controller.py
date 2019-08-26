from abc import ABCMeta, abstractmethod

class Controller(metaclass=ABCMeta):

    def __init__(self, model, field):
        field._controller = self
        self.model = model
        self.field = field

    @abstractmethod
    def check(self, value):
        pass

    @abstractmethod
    def set(self):
        pass
