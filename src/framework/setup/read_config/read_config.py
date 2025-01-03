from abc import ABC, abstractmethod

from framework.setup.read_config.load_file import ConfigContext, ConfigFactory


class IModelConfig(ABC):
    def __init__(self, config: dict):
        self.config = config

    @abstractmethod
    def unpack_config(self):
        pass


class WindowsModelConfig(IModelConfig):
    def __init__(self, config: dict):
        super().__init__(config)

        self.input_data = set()
        self.output_data = set()
        self.model_meta_data = dict()

    def unpack_config(self):
        self.input_data = self.config['input_data']



class GCPModelConfig(IModelConfig):
    # TODO: Implement this class and a run time selection design pattern for model config
    def unpack_config(self):
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
