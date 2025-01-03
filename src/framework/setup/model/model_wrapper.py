from abc import ABC, abstractmethod


class ModelWrapper(ABC):
    @abstractmethod
    def define_parameters(self):
        pass

    @abstractmethod
    def define_inputs(self):
        pass

    @abstractmethod
    def define_outputs(self):
        pass

    @abstractmethod
    def run_model(self):
        pass
