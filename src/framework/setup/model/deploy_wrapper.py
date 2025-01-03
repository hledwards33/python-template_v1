from framework.setup.model.model_wrapper import ModelWrapper
from framework.setup.read_config.read_config import ModelConfigDirector, WindowsModelConfigBuilder


class Model:
    def __init__(self):
        self._model_inputs = dict()
        self._model_outputs = dict()
        self._model_parameters = dict()

    @property
    def model_inputs(self):
        return self._model_inputs

    @model_inputs.setter
    def model_inputs(self, value):
        self._model_inputs = value

    @property
    def model_outputs(self):
        return self._model_outputs

    @model_outputs.setter
    def model_outputs(self, value):
        self._model_outputs = value

    @property
    def model_parameters(self):
        return self._model_parameters

    @model_parameters.setter
    def model_parameters(self, value):
        self._model_parameters = value


class ModelBuilder:
    def __init__(self, model_wrapper: ModelWrapper, model_config_path: str):
        self.model_wrapper = model_wrapper
        self.model_config = self.create_model_config(model_config_path)

        self.model = None

    def create_model(self):
        self.model = Model()

    def get_model(self):
        return self.model

    @staticmethod
    def create_model_config(model_config_path: str):
        # TODO: Add optionality to choose between different model config types
        config_builder = WindowsModelConfigBuilder(model_config_path)
        return ModelConfigDirector(config_builder).get_config()

    def combine_inputs(self):
        wrapper_inputs = self.model.define_inputs()
        config_inputs = self.model_config.input_data

        if set(wrapper_inputs.keys()) != set(config_inputs.keys()):
            raise KeyError("Model inputs do not match config inputs.")

        combined_inputs = {k: (v, wrapper_inputs[k]) for k, v in config_inputs.items()}
        self.model.model_inputs = combined_inputs

    def combine_outputs(self):
        wrapper_outputs = self.model.define_outputs()
        config_outputs = self.model_config.output_data

        if set(wrapper_outputs.keys()) != set(config_outputs.keys()):
            raise KeyError("Model outputs do not match config outputs.")

        combined_outputs = {k: (v, wrapper_outputs[k]) for k, v in config_outputs.items()}
        self.model.model_outputs = combined_outputs

    def combine_parameters(self):
        wrapper_parameters = self.model.define_parameters()
        config_parameters = self.model_config.model_parameters

        if set(wrapper_parameters.keys()) != set(config_parameters.keys()):
            raise KeyError("Model parameters do not match config parameters.")

        combined_parameters = {k: (v, wrapper_parameters[k]) for k, v in config_parameters.items()}
        self.model.model_parameters = combined_parameters


class ModelDirector:
    def __init__(self, builder: ModelBuilder):
        self.builder = builder

    def build_model(self):
        self.builder.create_model()
        self.builder.combine_inputs()
        self.builder.combine_outputs()
        self.builder.combine_parameters()
        return self.builder.get_model()
