from framework.model import BaseModel



class ExampleModel(BaseModel):

    def __init__(self, input_data: dict, parameters: dict):
        super(BaseModel, self).__init__(input_data)

    def run(self):

        return 0
