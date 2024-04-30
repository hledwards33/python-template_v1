from abc import ABC, abstractmethod

import yaml

from framework.data_scripts.read_inputs import InputData


class ModelWrapper(ABC):

    def __init__(self):
        pass

    @staticmethod
    def read_config(path: str) -> dict:
        config_dict = InputData.read_yaml(path=path)

        return config_dict

    @staticmethod
    def set_parameters():
        pass

    @staticmethod
    def data_pre_processing(data: dict) -> dict:
        pass

    @staticmethod
    def data_post_processing(data: dict) -> dict:
        pass

    def read_schemas(self):
        schema_dict = self.define_input_schemas()

        schema_dict = {key: InputData.read_json(path=val) for key, val in schema_dict.items()}

        return schema_dict

    @staticmethod
    def read_data(model_config: dict, file_schemas: dict) -> dict:

        data_dict = {}

        for key, val in model_config['inputs']:

            file_type = val.split(".")[-1]

            if file_type in ["csv", "zip"]:

                data_dict[key] = InputData.read_csv(path=val, schema=file_schemas[key])

            elif file_type in ["pqt", "parquet"]:

                data_dict[key] = InputData.read_parquet(path=val, schema=file_schemas[key])

        return data_dict

    @staticmethod
    def write_data(path: str, file_schemas: dict) -> dict:
        pass

    @abstractmethod
    def define_input_schemas(self):
        pass

    @abstractmethod
    def define_output_schemas(self):
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
