import json
from abc import ABC, abstractmethod

import yaml

from framework.setup.read_config.type_complexities import ConfigExtension


class IReadConfig(ABC):
    def __init__(self, config_path: str):
        self.config_path = config_path

    @abstractmethod
    def read_config(self) -> dict:
        pass


class ReadJsonConfig(IReadConfig):
    def read_config(self) -> dict:
        with open(self.config_path, 'r') as file:
            result = json.load(file)
        return result


class ReadYamlConfig(IReadConfig):
    def read_config(self) -> dict:
        with open(self.config_path, 'r') as file:
            result = yaml.safe_load(file)
        return result


class ConfigContext:
    def __init__(self, config_path: str):
        self.config_path = config_path
        self.config_extension = config_path.split('.')[-1]


class ConfigFactory:
    @staticmethod
    def create_config_reader(context: ConfigContext) -> IReadConfig:
        match context.config_extension:
            case ConfigExtension.JSON.value:
                return ReadJsonConfig(context.config_path)
            case ConfigExtension.YAML.value | ConfigExtension.YAML_SHORT.value:
                return ReadYamlConfig(context.config_path)
            case _:
                raise ValueError(f'Invalid config file extension: {context.config_extension}.')
