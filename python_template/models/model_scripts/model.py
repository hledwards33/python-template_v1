from abc import ABC, abstractmethod


class BaseModel(ABC):

    def __init__(self, input_data: dict):
        self.model_data = input_data
        self.run_model = self.run()

    @abstractmethod
    def run(self):
        pass
