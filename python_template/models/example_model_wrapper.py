from model_scripts.example_model.example_model import ExampleModel
from model_wrapper import ModelWrapper


class ExampleWrapper:

    @staticmethod
    def run():
        data = ModelWrapper.read_data()

        parameters = ModelWrapper.set_parameters_from_dataframe()

        model_result = ExampleModel.run_model()


if __name__ == "__main__":
    ExampleWrapper.run()