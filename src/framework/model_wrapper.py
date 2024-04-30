import pandas as pd
import yaml


class ModelWrapper:

    def __init__(self):
        pass

    @staticmethod
    def read_config():
        pass

    @staticmethod
    def set_parameters_from_dataframe(data: pd.DataFrame) -> pd.DataFrame:
        pass

    @staticmethod
    def data_pre_processing(data: dict) -> dict:
        pass

    @staticmethod
    def data_post_processing(data: dict) -> dict:
        pass

    @staticmethod
    def read_data(path: str, file_schemas: dict) -> dict:
        pass

    @staticmethod
    def write_data(path: str, file_schemas: dict) -> dict:
        pass


class DeployWrapper:

    def __init__(self):
        pass

    def run_model(self, model_wrapper: ModelWrapper, sys_config: str, model_config: str):
        sys_config = self.read_config(sys_config)
        model_config = self.read_config(model_config)

    @staticmethod
    def read_config(config_path: str) -> dict:
        with open(config_path, 'r') as file:
            config_dict = yaml.safe_load(file)

        return config_dict
