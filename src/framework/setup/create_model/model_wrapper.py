from abc import ABC, abstractmethod
from enum import Enum

from framework.setup.create_model.model import IModel


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
    def define_model(self) -> IModel:
        pass

    @staticmethod
    def run_model(model: IModel) -> dict:
        result = model.run()
        return result
