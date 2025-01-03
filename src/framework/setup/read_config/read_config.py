from abc import ABC, abstractmethod

from framework.setup.read_config.load_file import ConfigContext, ConfigFactory, IReadConfig


class IModelConfigBuilder(ABC):
    def __init__(self, config_path: str):
        self.config = self.set_config_reader(config_path).read_config()

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
    def __init__(self, context):
        super().__init__(context)

    def define_input_data(self):
        return self.config['input_data']

    def define_output_data(self):
        return self.config['output_data']

    def define_model_parameters(self):
        return self.config['model_parameters']


class GCPModelConfigBuilder(IModelConfigBuilder):
    # TODO: Implement this class and a run time selection design pattern for model config
    pass


class ModelConfigDirector:
    def __init__(self, config_path: str):
        self.config = self.get_config(config_path)

    @staticmethod
    def get_config(config_path: str):
        context = ConfigContext(config_path)
        return ConfigFactory.create_config_reader(context).read_config()

    def unpack_config(self):
        return self.config
