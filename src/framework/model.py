from abc import ABC, abstractmethod


class BaseModel(ABC):

    def __init__(self, input_data: dict, parameters: dict):
        self.model_data: dict = input_data
        self.model_parameters: dict = parameters

    @abstractmethod
    def run(self):
        pass


