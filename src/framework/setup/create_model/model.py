from abc import ABC, abstractmethod


class IModel(ABC):
    def __init__(self, input_data: dict, parameters: dict):
        self._data = input_data
        self._parameters = parameters

    @abstractmethod
    def run(self) -> dict:
        pass
