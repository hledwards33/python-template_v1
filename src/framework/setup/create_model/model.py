from abc import ABC, abstractmethod


class IModel(ABC):
    def __init__(self, input_data: dict, parameters: dict):
        self._data = input_data
        self._parameters = parameters

    @property
    def data(self):
        return self._data

    @property
    def parameters(self):
        return self._parameters

    @data.setter
    def data(self, value):
        self._data = value

    @parameters.setter
    def parameters(self, value):
        self._parameters = value

    @abstractmethod
    def run(self) -> dict:
        pass
