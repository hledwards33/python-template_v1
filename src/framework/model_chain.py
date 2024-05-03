import importlib
import os

from framework.model_wrapper import DeployWrapper
from framework.setup.read_write_data import read_yaml
from framework.setup.log_format import headers


class ModelChain:
    PY_FILE_DIR = os.path.abspath(os.path.dirname(__file__))
    PY_ROOT_DIR = os.path.abspath(os.path.join(PY_FILE_DIR, "../"))
    # TODO amend in final version
    PY_REPO_DIR = os.path.dirname(PY_ROOT_DIR)

    def __init__(self, config_path: str):
        self.sys_config_path = self.read_config(config_path)['config']['sys_config']
        self.chain_config = self.read_config(config_path)['models']

    def read_config(self, path: str) -> dict:
        path = os.path.join(self.__class__.PY_REPO_DIR, path)
        config_dict = read_yaml(path=path)

        return config_dict

    def get_model_class(self, model_config: dict):
        model_class = getattr(importlib.import_module(model_config['model_path']), model_config['model'])
        return model_class

    def run_chain(self):
        for model_name, model_config in self.chain_config.items():
            headers(f"Executing Model '{model_name}'")

            model_class = self.get_model_class(model_config)

            model = DeployWrapper(model_class, self.sys_config_path,
                                  model_config['config'])
            model.run_model()


if __name__ == "__main__":
    _config_path = "config/model_config/model_chains/example_model_chain.yml"

    model_chain = ModelChain(_config_path)

    model_chain.run_chain()
