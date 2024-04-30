import logging
import os
from abc import ABC, abstractmethod

from framework.setup import read_write_data
from framework.setup.log_format import headers

logger = logging.getLogger()


class ModelWrapper(ABC):

    def __init__(self):
        self.data_dict = {}

    @property
    def data_dict(self):
        return self._data_dict

    @data_dict.setter
    def data_dict(self, value: dict):
        self._data_dict = value

    @staticmethod
    def set_parameters():
        pass

    @staticmethod
    def read_schemas(schema_dict: dict) -> dict:

        schema_dict = {key: read_write_data.read_json(path=val) for key, val in schema_dict.items()}

        return schema_dict

    @staticmethod
    def read_data_to_pandas(model_config: dict, file_schemas: dict, base_path: str) -> dict:

        data_dict = {}

        for key, val in model_config['inputs'].items():

            logger.info(f"Reading dataset {key}.")

            schema = read_write_data.convert_schema_pandas(file_schemas[key])
            file_type = val.split(".")[-1]
            val = os.path.join(base_path, val)

            if file_type in ["csv", "zip"]:

                data_dict[key] = read_write_data.read_csv_to_pandas(path=val, schema=schema)

            elif file_type in ["pqt", "parquet"]:

                data_dict[key] = read_write_data.read_parquet_to_pandas(path=val, schema=schema)

            logger.info(
                f"Dataset {key} is loaded with dimensions: {len(data_dict[key].columns)} x {len(data_dict[key])}")

        return data_dict

    @staticmethod
    def read_data_to_spark(model_config: dict, file_schemas: dict) -> dict:
        pass

    @staticmethod
    def write_data_from_pandas(data_dict: dict, model_config: dict, file_schemas: dict, base_path: str):

        for key, val in model_config['model_data']['outputs']:

            logger.info(f"Writing dataset {key} with dimensions {len(data_dict[key].columns)} x {len(data_dict[key])}.")

            schema = file_schemas[key]
            file_type = val.split(".")[-1]
            val = os.path.join(base_path, val)

            if file_type in ["csv"]:

                read_write_data.write_csv_from_pandas(data=data_dict[key], path=val, schema=schema)

            elif file_type in ["pqt", "parquet"]:

                read_write_data.write_parquet_from_pandas(data=data_dict[key], path=val, schema=schema)

            elif file_type in ['zip']:

                read_write_data.write_zip_from_pandas(path=val, schema=schema)

            logger.info(f"Dataset {key} has been saved.")

    @staticmethod
    def write_data_from_spark(model_config: dict, file_schemas: dict):
        pass

    @staticmethod
    def data_pre_processing() -> dict:
        pass

    @staticmethod
    def data_post_processing() -> dict:
        pass

    @abstractmethod
    def define_input_schemas(self) -> dict:
        pass

    @abstractmethod
    def define_output_schemas(self) -> dict:
        pass

    @abstractmethod
    def run_model(self) -> dict:
        pass


class DeployWrapper:
    PY_FILE_DIR = os.path.abspath(os.path.dirname(__file__))
    PY_ROOT_DIR = os.path.abspath(os.path.join(PY_FILE_DIR, ".."))
    PY_REPO_DIR = os.path.dirname(PY_ROOT_DIR)

    def __init__(self, model_wrapper: ModelWrapper, sys_config: str, model_config: str):
        self.model_wrapper = model_wrapper()
        self.sys_config = self.read_config(sys_config)
        self.model_config = self.read_config(model_config)

    def get_data_dir(self):
        return os.path.join(self.__class__.PY_REPO_DIR, self.sys_config['data']['data_folder'])

    def run_model(self):

        headers.info("Reading Input Data.")
        input_data = self.get_inputs()

        self.model_wrapper.data_dict = input_data

        headers.info("Executing Model.")
        output_data = self.model_wrapper.run_model()

        headers.info("Writing Output Data.")
        self.post_outputs(data_dict=output_data)

    def post_outputs(self, data_dict: dict):
        output_schemas = self.model_wrapper.read_schemas(schema_dict=self.model_wrapper.define_output_schemas())

        conformance_errors = self.run_schema_conformance(data_dict=data_dict, schema_dict=output_schemas)

        error_count = sum([len(error) for dataset_errors in conformance_errors.values() for error in
                           dataset_errors.values()])

        if error_count > 0:
            headers.info("Data Conformance Errors.")
            for dataset, dataset_errors in conformance_errors.items():
                for error_type, error in dataset_errors.items():
                    logger.info(f"Dataset {dataset} has {error_type}: {error}")

            raise TypeError(f"Incorrect DataTypes and/or DataColumns see above logs.")

        if self.model_config['parameters']['model_parameters']['type'] == "pandas":

            self.model_wrapper.write_data_from_pandas(data_dict=data_dict, model_config=self.model_config,
                                                      file_schemas=output_schemas, base_path=self.get_data_dir())

        elif self.model_config['parameters']['model_parameters']['type'] == "pyspark":

            self.model_wrapper.write_data_from_spark(data_dict=data_dict, model_config=self.model_config,
                                                     file_schemas=output_schemas, base_path=self.get_data_dir())

    def get_inputs(self) -> dict:
        input_schemas = self.model_wrapper.read_schemas(schema_dict=self.model_wrapper.define_input_schemas())

        if self.model_config['parameters']['model_parameters']['type'] == "pandas":

            input_data = self.model_wrapper.read_data_to_pandas(model_config=self.model_config['model_data'],
                                                                file_schemas=input_schemas,
                                                                base_path=self.get_data_dir())

        elif self.model_config['parameters']['model_parameters']['type'] == "pyspark":

            input_data = self.model_wrapper.read_data_to_spark(model_config=self.model_config['model_data'],
                                                               file_schemas=input_schemas,
                                                               base_path=self.get_data_dir())

        else:
            raise ImportError('Parameter "Type" is defined incorrectly. Type can take values ["pandas", "pyspark"] and '
                              f'is currently set to {self.sys_config["model_parameters"]["type"]}.')

        return input_data

    def run_schema_conformance(self, data_dict: dict, schema_dict: dict) -> dict:
        data_errors = {}

        for key, val in data_dict.items():

            if self.model_config['parameters']['model_parameters']['type'] == "pandas":

                schema = read_write_data.convert_schema_output_pandas(schema_dict[key])

                data_errors[key] = read_write_data.schema_conformance_pandas(data=val, schema=schema,
                                                                             dataframe_name=key)

            elif self.model_config['parameters']['model_parameters']['type'] == "pandas":

                schema = read_write_data.convert_schema_spark(schema_dict[key])

                data_errors[key] = read_write_data.schema_conformance_spark(data=val, schema=schema, dataframe_name=key)

        return data_errors

    def read_config(self, path: str) -> dict:
        path = os.path.join(self.__class__.PY_REPO_DIR, path)
        config_dict = read_write_data.read_yaml(path=path)

        return config_dict
