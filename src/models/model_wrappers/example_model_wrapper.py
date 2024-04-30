from framework.model_wrapper import ModelWrapper, DeployWrapper
from models.model_scripts.example_model.example_model import ExampleModel as Model


class ExampleWrapper(ModelWrapper):

    def __init__(self):
        super(ModelWrapper, self).__init__()

    def run(self):
        input_data = self.read_data()

        parameters = self.set_parameters_from_dataframe()

        model_result = Model(input_data, parameters).run()

        return model_result


if __name__ == "__main__":
    DeployWrapper.run_model(model_wrapper=ExampleWrapper, sys_config='config/system_config.yml',
                            model_config='config/model_config/example_model_config.yml')
