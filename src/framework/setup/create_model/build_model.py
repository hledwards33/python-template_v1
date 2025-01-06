import os

from framework.setup.create_model.model_wrapper import IModelWrapper
from framework.setup.read_config.read_config import ModelConfigDirector, WindowsModelConfigBuilder


class ModelMetaData:
    def __init__(self):
        self._model_inputs: dict = dict()
        self._model_outputs: dict = dict()
        self._model_parameters: dict = dict()
        self._model_type: str = ""
        self._model_name: str = ""
        self._run_model = None

    @property
    def run_model(self):
        return self._run_model

    @run_model.setter
    def run_model(self, value):
        self._run_model = value

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

    @property
    def model_type(self):
        return self._model_type

    @model_type.setter
    def model_type(self, value):
        self._model_type = value

    @property
    def model_name(self):
        return self._model_name

    @model_name.setter
    def model_name(self, value):
        self._model_name = value


class ModelBuilder:
    __DATA_PATH = os.path.join(os.getcwd(), "data")

    def __init__(self, model_wrapper: IModelWrapper, model_config_path: str):
        self.model_wrapper = model_wrapper
        self.model_config = self.create_model_config(model_config_path)

        self.model = None

    def create_model(self):
        self.model = ModelMetaData()

    def get_model(self):
        return self.model

    @staticmethod
    def create_model_config(model_config_path: str):
        # TODO: Add optionality to choose between different model config types
        config_builder = WindowsModelConfigBuilder(model_config_path)
        return ModelConfigDirector(config_builder).get_config()

    def combine_inputs(self):
        wrapper_inputs = self.model_wrapper.define_inputs()
        config_inputs = self.model_config.input_data

        if set(wrapper_inputs.keys()) != set(config_inputs.keys()):
            raise KeyError("Model inputs do not match config inputs.")

        combined_inputs = {k: (self.combine_config_paths(v), self.combine_wrapper_paths(wrapper_inputs[k])) for k, v in
                           config_inputs.items()}
        self.model.model_inputs = combined_inputs

    def combine_config_paths(self, path: str):
        result = os.path.join(self.__DATA_PATH, path)
        return os.path.normpath(result)

    @staticmethod
    def combine_wrapper_paths(paths: tuple):
        result = os.path.join(os.path.split(paths[0].__file__)[0], paths[1])
        return os.path.normpath(result)

    def combine_outputs(self):
        wrapper_outputs = self.model_wrapper.define_outputs()
        config_outputs = self.model_config.output_data

        if set(wrapper_outputs.keys()) != set(config_outputs.keys()):
            raise KeyError("Model outputs do not match config outputs.")

        combined_outputs = {k: (v, wrapper_outputs[k]) for k, v in config_outputs.items()}
        self.model.model_outputs = combined_outputs

    def combine_parameters(self):
        wrapper_parameters = self.model_wrapper.define_parameters()
        config_parameters = self.model_config.model_parameters['model_parameters']

        if set(wrapper_parameters.keys()) != set(config_parameters.keys()):
            raise KeyError("Model parameters do not match config parameters.")

        combined_parameters = {k: (v, wrapper_parameters[k]) for k, v in config_parameters.items()}
        self.model.model_parameters = combined_parameters

    def define_model_attributes(self):
        self.model.model_type = self.model_config.model_parameters['model_type']
        self.model.model_name = self.model_config.model_parameters['model_id']

    def define_model(self):
        self.model.run_model = self.model_wrapper.run_model


class ModelDirector:
    def __init__(self, builder: ModelBuilder):
        self.builder = builder

    def build_model(self):
        self.builder.create_model()
        self.builder.combine_inputs()
        self.builder.combine_outputs()
        self.builder.combine_parameters()
        self.builder.define_model_attributes()
        self.builder.define_model()
        return self.builder.get_model()
