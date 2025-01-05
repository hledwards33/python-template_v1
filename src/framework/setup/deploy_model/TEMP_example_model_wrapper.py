from framework.setup.create_model.model_wrapper import ModelWrapper


class ExampleModel(ModelWrapper):
    def define_parameters(self) -> dict:
        return {"example_parameter": "example_value"}

    def define_inputs(self) -> dict:
        return {"example_input": "",
                "example_input_2": ""}

    def define_outputs(self) -> dict:
        return {"example_output": "",
                "example_output_2": ""}

    def run_model(self) -> dict:
        return {}
