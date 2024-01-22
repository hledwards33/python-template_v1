from model_scripts.example_model.example_model import ExampleModel as Model
from model_wrapper import ModelWrapper


class ExampleWrapper:

    @staticmethod
    def run():
        input_data = ModelWrapper.read_data()

        parameters = ModelWrapper.set_parameters_from_dataframe()

        model_result = Model(input_data, parameters).run()

        return model_result

if __name__ == "__main__":
    ExampleWrapper.run()