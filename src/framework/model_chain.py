import importlib
import os

from config import PY_REPO_DIR
from framework.model_wrapper import DeployWrapper
from framework.model_wrapper import ModelWrapper
from framework.setup.log_format import headers
from framework.setup.read_write_data import read_yaml
from config import PY_ROOT_DIR


class ModelChain:

    def __init__(self, config_path: str):
        self.sys_config_path = self.read_config(config_path)['config']['sys_config']
        self.chain_config = self.read_config(config_path)['models']

    @staticmethod
    def read_config(path: str) -> dict:
        path = os.path.join(PY_ROOT_DIR, path)
        config_dict = read_yaml(path=path)

        return config_dict

    @staticmethod
    def get_model_class(model_config: dict) -> ModelWrapper:
        model_class = getattr(importlib.import_module(model_config['model_path']), model_config['model'])
        return model_class

    def run_chain(self) -> None:
        for model_name, model_config in self.chain_config.items():
            headers(f"Executing Model '{model_name}'")

            model_class = self.get_model_class(model_config)

            DeployWrapper(model_class, self.sys_config_path,
                          model_config['config']).run_model()
