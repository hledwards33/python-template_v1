from framework.model import BaseModel


class Model:

    def __int__(self, data_dict: dict):
        self.model = ExampleModel(input_data=data_dict, parameters={})

        self.execute = self.execute()

    def execute(self):
        result = self.model.run()

        return result


class ExampleModel(BaseModel):

    def __init__(self, input_data: dict, parameters: dict = {}):
        super().__init__(input_data, parameters)

    def run(self):
        return {'ecl_data': self.model_data['pd_data']}
