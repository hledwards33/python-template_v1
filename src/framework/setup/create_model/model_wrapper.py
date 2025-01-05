from abc import ABC, abstractmethod
from enum import Enum


class ParameterTypes(Enum):
    INTEGER = "integer"
    FLOAT = "float"
    STRING = "string"
    DATE = "date"


class IModelWrapper(ABC):
    def __init__(self):
        self.parameter_types = ParameterTypes

    @abstractmethod
    def define_parameters(self) -> dict:
        pass

    @abstractmethod
    def define_inputs(self) -> dict:
        pass

    @abstractmethod
    def define_outputs(self) -> dict:
        pass

    @abstractmethod
    def run_model(self) -> dict:
        pass
