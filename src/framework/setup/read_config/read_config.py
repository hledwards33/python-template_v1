from abc import ABC, abstractmethod

from framework.setup.read_config.load_file import ConfigContext, ConfigFactory, IReadConfig


class ModelConfig:
    def __init__(self):
        self._input_data = dict()
        self._output_data = dict()
        self._model_parameters = dict()

    @property
    def input_data(self):
        return self._input_data

    @input_data.setter
    def input_data(self, value):
        self._input_data = value

    @property
    def output_data(self):
        return self._output_data

    @output_data.setter
    def output_data(self, value):
        self._output_data = value

    @property
    def model_parameters(self):
        return self._model_parameters

    @model_parameters.setter
    def model_parameters(self, value):
        self._model_parameters = value


class IModelConfigBuilder(ABC):
    def __init__(self, config_path: str):
        self.raw_config = self.set_config_reader(config_path).read_config()
        self.model_config = None

    def create_model_config(self):
        self.model_config = ModelConfig()

    def get_model_config(self):
        return self.model_config

    @staticmethod
    def set_config_reader(config_path: str) -> IReadConfig:
        config_context = ConfigContext(config_path)
        return ConfigFactory.create_config_reader(config_context)

    @abstractmethod
    def define_input_data(self):
        pass

    @abstractmethod
    def define_output_data(self):
        pass

    @abstractmethod
    def define_model_parameters(self):
        pass


class WindowsModelConfigBuilder(IModelConfigBuilder):

    def define_input_data(self):
        self.model_config.input_data = self.raw_config['model_data']['inputs']

    def define_output_data(self):
        self.model_config.output_data = self.raw_config['model_data']['outputs']

    def define_model_parameters(self):
        self.model_config.model_parameters = self.raw_config['parameters']


class GCPModelConfigBuilder(IModelConfigBuilder):
    # TODO: Implement this class and a run time selection design pattern for model config
    def define_input_data(self):
        pass

    def define_output_data(self):
        pass

    def define_model_parameters(self):
        pass


class ModelConfigDirector:
    def __init__(self, builder: IModelConfigBuilder):
        self.builder = builder

    def get_config(self):
        self.builder.create_model_config()
        self.builder.define_model_parameters()
        self.builder.define_input_data()
        self.builder.define_output_data()
        return self.builder.get_model_config()
