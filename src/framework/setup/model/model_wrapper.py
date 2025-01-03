from abc import ABC, abstractmethod


class ModelWrapper(ABC):
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
