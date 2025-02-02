import datetime
import logging
import os
import time
from abc import ABC, abstractmethod

import pandas as pd

from config import PY_ROOT_DIR
from framework.setup import read_write_data
from framework.setup.log_format import (headers, create_logging_file, remove_handler,
                                        create_logging_file_handler_detailed, initiate_logger)

initiate_logger()
logger = logging.getLogger()


class ModelWrapper(ABC):

    def __init__(self):
        self.data_dict = {}
        self.parameters = {}

    @property
    def parameters(self) -> dict:
        return self._parameters

    @parameters.setter
    def parameters(self, value: dict) -> None:
        self._parameters = value

    @property
    def data_dict(self) -> dict:
        return self._data_dict

    @data_dict.setter
    def data_dict(self, value: dict) -> None:
        self._data_dict = value

    @staticmethod
    def read_schemas(schema_dict: dict) -> dict:

        schema_dict = {key: read_write_data.read_json(path=val) for key, val in schema_dict.items()}

        return schema_dict

    @staticmethod
    def read_data_to_pandas(model_config: dict, file_schemas: dict, base_path: str) -> dict:

        data_dict = {}

        for key, val in model_config['inputs'].items():

            logger.info(f"Reading dataset '{key}'.")

            schema = read_write_data.convert_schema_pandas(file_schemas[key])
            file_type = val.split(".")[-1]
            val = os.path.join(base_path, val)

            if file_type in ["csv", "zip"]:

                data_dict[key] = read_write_data.read_csv_to_pandas(path=val, schema=schema)

            elif file_type in ["pqt", "parquet"]:

                data_dict[key] = read_write_data.read_parquet_to_pandas(path=val, schema=schema)

            logger.info(
                f"Dataset '{key}' is loaded with dimensions: {len(data_dict[key].columns)} x {len(data_dict[key])}.")

        return data_dict

    @staticmethod
    def read_data_to_spark(model_config: dict, file_schemas: dict) -> dict:
        pass

    @staticmethod
    def write_data_from_pandas(data_dict: dict, model_config: dict, file_schemas: dict, base_path: str) -> None:

        for key, val in model_config['outputs'].items():

            logger.info(f"Writing dataset '{key}' with dimensions {len(data_dict[key].columns)} x "
                        f"{len(data_dict[key])}.")

            schema = file_schemas[key]
            file_type = val.split(".")[-1]
            val = os.path.join(base_path, val)

            if file_type in ["csv"]:

                read_write_data.write_csv_from_pandas(data=data_dict[key], path=val, schema=schema)

            elif file_type in ["pqt", "parquet"]:

                read_write_data.write_parquet_from_pandas(data=data_dict[key], path=val, schema=schema)

            elif file_type in ['zip']:

                read_write_data.write_zip_from_pandas(data=data_dict[key], path=val, schema=schema)

            logger.info(f"Dataset '{key}' has been saved.")

    @staticmethod
    def write_data_from_spark(model_config: dict, file_schemas: dict) -> None:
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
    def define_parameter_schemas(self) -> tuple:
        pass

    @abstractmethod
    def run_model(self) -> dict:
        pass


class DeployWrapper:

    def __init__(self, model_wrapper: ModelWrapper, sys_config: str, model_config: str):
        self.model_wrapper = model_wrapper()
        self.sys_config = self.read_config(sys_config)
        self.model_config = self.read_config(model_config)
        self.start_logging()

    def start_logging(self) -> None:
        name = self.model_config['parameters']['model_parameters']['log_name']
        path = os.path.join(PY_ROOT_DIR, self.model_config['parameters']['model_parameters']['log_location'])
        create_logging_file(create_logging_file_handler_detailed, path, name)

    def stop_logging(self) -> None:
        name = self.model_config['parameters']['model_parameters']['log_name']
        remove_handler(name)

    def get_data_dir(self) -> os.path:
        return os.path.join(PY_ROOT_DIR, self.sys_config['data']['data_folder'])

    @staticmethod
    def config_logs(log_config: dict) -> None:
        headers("Model Configuration")

        logger.info(f"This log was created {datetime.date.today()} {datetime.datetime.now().strftime('%H:%M:%S')}.")
        logging.info(f"Model Log file pattern: {log_config['log_location']}/{log_config['log_name']}.")
        logging.info(f"Model Type is {log_config['model_type']}.")
        logging.info(f"Model is running on {log_config['type']}.")
        logger.info(f"Model ID '{log_config['model_id']}' is Running.")

    def run_model(self) -> None:
        start = time.perf_counter()

        self.config_logs(self.model_config['parameters']['model_parameters'])

        headers("Reading Input Data")
        input_data = self.get_inputs()
        parameters = self.get_parameters()

        self.model_wrapper.data_dict = input_data
        self.model_wrapper.parameters = parameters

        headers("Executing Model")
        output_data = self.model_wrapper.run_model()

        headers("Writing Output Data")
        self.post_outputs(data_dict=output_data)

        logger.info("Output Data Saved Successfully.")
        headers(f"Model '{self.model_config['parameters']['model_parameters']['model_id']}' Ran Successfully")

        end = time.perf_counter()
        logger.info(f"Model execution time: {end - start:0.4f} seconds.")

        self.stop_logging()

    def get_parameters_from_file(self) -> pd.DataFrame:
        # Reading in parameters file defined in model config yaml
        parameters_path = self.model_config['parameters']['model_parameters']['parameters_file']

        if parameters_path != "":

            if self.model_wrapper.define_parameter_schemas() is not None:

                parameters_schema = read_write_data.read_json(path=self.model_wrapper.define_parameter_schemas())

                parameters_path = os.path.join(self.get_data_dir(), parameters_path)
                parameters_schema = read_write_data.convert_schema_pandas(parameters_schema)
                parameters = read_write_data.read_csv_to_pandas(path=parameters_path, schema=parameters_schema)

            else:
                logger.error("No parameters schema file has been passed to the model framework. See method "
                             "define_parameter_schemas in model wrapper.")

        else:
            logger.info("No parameters input file is being used within this model.")

            parameters = pd.DataFrame()

        return parameters

    def get_optional_parameters(self) -> pd.DataFrame:
        # Reading in optional parameters defined in model config yaml
        optional_parameters = self.model_config['parameters']['model_parameters']['optional']

        # Add optional parameters from the config file
        if optional_parameters is not None:
            optional_parameters = {
                'parameter': [key for key in optional_parameters.keys()],
                'value': [val for val in optional_parameters.values()]
            }

            optional_parameters = pd.DataFrame.from_dict(optional_parameters)

        else:
            logger.info("No optional parameters are being used within this model.")

            optional_parameters = pd.DataFrame()

        return optional_parameters

    def get_parameters(self) -> pd.DataFrame:

        # Get parameters from passed file
        file_parameters = self.get_parameters_from_file()

        # Reading in optional parameters defined in model config yaml
        optional_parameters = self.get_optional_parameters()

        # Combine the file parameters and optional parameters
        parameters = pd.concat([file_parameters, optional_parameters], axis=0, ignore_index=True)

        return parameters

    def check_data_conformance(self, data_dict: dict, output_schemas: dict) -> None:

        conformance_errors = self.run_schema_conformance(data_dict=data_dict, schema_dict=output_schemas)

        error_count = sum([len(error) for dataset_errors in conformance_errors.values() for error in
                           dataset_errors.values()])

        if error_count > 0:
            headers("Data Conformance Errors")
            for dataset, dataset_errors in conformance_errors.items():
                for error_type, error in dataset_errors.items():
                    logger.info(f"Dataset {dataset} has {error_type}: {error}.")

            raise TypeError(f"Incorrect DataTypes and/or DataColumns see above logs.")

    def post_outputs(self, data_dict: dict) -> None:

        if not isinstance(data_dict, dict):
            raise TypeError(f"Model output is not returning a dictionary of dataframes and is instead returning a "
                            f"{type(data_dict).__name__}.")

        output_schemas = self.model_wrapper.read_schemas(schema_dict=self.model_wrapper.define_output_schemas())

        self.memory_usage(data_dict, 'output')

        self.check_data_conformance(data_dict, output_schemas)

        if self.model_config['parameters']['model_parameters']['type'].lower() == "pandas":

            self.model_wrapper.write_data_from_pandas(data_dict=data_dict, model_config=self.model_config['model_data'],
                                                      file_schemas=output_schemas, base_path=self.get_data_dir())

        elif self.model_config['parameters']['model_parameters']['type'].lower() == "pyspark":

            self.model_wrapper.write_data_from_spark(data_dict=data_dict, model_config=self.model_config['model_data'],
                                                     file_schemas=output_schemas, base_path=self.get_data_dir())

    def get_inputs(self) -> dict:
        input_schemas = self.model_wrapper.read_schemas(schema_dict=self.model_wrapper.define_input_schemas())

        if self.model_config['parameters']['model_parameters']['type'].lower() == "pandas":

            input_data = self.model_wrapper.read_data_to_pandas(model_config=self.model_config['model_data'],
                                                                file_schemas=input_schemas,
                                                                base_path=self.get_data_dir())

        elif self.model_config['parameters']['model_parameters']['type'].lower() == "pyspark":

            input_data = self.model_wrapper.read_data_to_spark(model_config=self.model_config['model_data'],
                                                               file_schemas=input_schemas,
                                                               base_path=self.get_data_dir())

        else:
            raise ImportError('Parameter "Type" is defined incorrectly. Type can take values ["pandas", "pyspark"] and '
                              f'is currently set to {self.sys_config["model_parameters"]["type"]}.')

        self.memory_usage(input_data, 'input')

        return input_data

    @staticmethod
    def memory_usage(data_dict: dict, data_type: str) -> None:
        memory_usage = sum([df.memory_usage(index=True).sum() for df in data_dict.values()])
        logger.info(f"Total memory usage of the {data_type} data is {memory_usage * 0.0000000001}GB.")

    def run_schema_conformance(self, data_dict: dict, schema_dict: dict) -> dict:
        data_errors = {}

        for key, val in data_dict.items():

            if self.model_config['parameters']['model_parameters']['type'].lower() == "pandas":

                schema = read_write_data.convert_schema_output_pandas(schema_dict[key])

                data_errors[key] = read_write_data.schema_conformance_pandas(data=val, schema=schema,
                                                                             dataframe_name=key)

            elif self.model_config['parameters']['model_parameters']['type'].lower() == "spark":

                schema = read_write_data.convert_schema_spark(schema_dict[key])

                data_errors[key] = read_write_data.schema_conformance_spark(data=val, schema=schema, dataframe_name=key)

        return data_errors

    @staticmethod
    def read_config(path: str) -> dict:
        path = os.path.join(PY_ROOT_DIR, path)
        config_dict = read_write_data.read_yaml(path=path)

        return config_dict
