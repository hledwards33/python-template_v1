from abc import ABC, abstract_method

class BaseModel:

    def __init__(self, input_data: dict):
        self.model_data = input_data

    def run(self):
        pass
