from framework.setup.model.model_wrapper import ModelWrapper
from framework.setup.read_config.read_config import ModelConfigDirector


class ModelBuilder:
    def __init__(self, model: ModelWrapper, model_config: str):
        self.model = model
        self.model_config = model_config

    def get_model_config(self):
        config_builder = ModelConfigDirector(self.model_config)


    def combine_inputs(self):
        wrapper_inputs = self.model.define_inputs()
        config_inputs = self.model_config['inputs']