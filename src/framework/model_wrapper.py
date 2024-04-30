from abc import ABC, abstractmethod

from framework.data_scripts.read_inputs import InputOutputData


class ModelWrapper(ABC):

    def __init__(self):
        pass

    @staticmethod
    def set_parameters():
        pass

    @staticmethod
    def read_schemas(schema_dict: dict) -> dict:

        schema_dict = {key: InputOutputData.read_json(path=val) for key, val in schema_dict.items()}

        return schema_dict

    @staticmethod
    def read_data_to_pandas(model_config: dict, file_schemas: dict) -> dict:

        data_dict = {}

        for key, val in model_config['inputs']:

            schema = InputOutputData.convert_schema_pandas(file_schemas[key])
            file_type = val.split(".")[-1]

            if file_type in ["csv", "zip"]:

                data_dict[key] = InputOutputData.read_csv_to_pandas(path=val, schema=schema)

            elif file_type in ["pqt", "parquet"]:

                data_dict[key] = InputOutputData.read_parquet_to_pandas(path=val, schema=schema)

        return data_dict

    @staticmethod
    def read_data_to_spark(model_config: dict, file_schemas: dict) -> dict:
        # TODO: fill in the method
        pass

    @staticmethod
    def write_data_from_pandas(model_config: dict, file_schemas: dict):

        for key, val in model_config['inputs']:

            schema = InputOutputData.convert_schema_pandas(file_schemas[key])
            file_type = val.split(".")[-1]

            if file_type in ["csv"]:

                InputOutputData.write_csv_from_pandas(path=val, schema=schema)

            elif file_type in ["pqt", "parquet"]:

                InputOutputData.write_parquet_from_pandas(path=val, schema=schema)

            elif file_type in ['zip']:

                InputOutputData.write_zip_from_pandas(path=val, schema=schema)

    @staticmethod
    def write_data_from_spark(model_config: dict, file_schemas: dict):
        # TODO: Fill in this method
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

    def __init__(self, model_wrapper: ModelWrapper, sys_config: str, model_config: str):
        self.model_wrapper = model_wrapper
        self.sys_config = self.read_config(sys_config)
        self.model_config = self.read_config(model_config)

    def run_model(self):
        input_data = self.get_inputs()

        output_data = self.run_model(input_data)

        self.post_outputs(data=output_data)

    def post_outputs(self, data_dict: dict):
        output_schemas = self.model_wrapper.read_schemas(schema_dict=self.model_wrapper.define_output_schemas())

        conformance_errors = self.run_schema_conformance(data_dict=data_dict, schema_dict=output_schemas)

        error_count = sum([len(error) for dataset_errors in conformance_errors.items() for error in
                           dataset_errors.items()])

        if error_count > 0:
            # TODO: Log all errors
            raise TypeError(f"Incorrect DataTypes and/or DataColumns see above logs.")

        if self.sys_config['model_parameters']['type'] == "pandas":

            self.model_wrapper.write_data_from_pandas(model_config=self.model_config, file_schemas=output_schemas)

        elif self.sys_config['model_parameters']['type'] == "pyspark":

            self.model_wrapper.write_data_from_spark(model_config=self.model_config, file_schemas=output_schemas)

    def get_inputs(self) -> dict:
        input_schemas = self.model_wrapper.read_schemas(schema_dict=self.model_wrapper.define_input_schemas())

        if self.sys_config['model_parameters']['type'] == "pandas":

            input_data = self.model_wrapper.read_data_to_pandas(model_config=self.model_config,
                                                                file_schemas=input_schemas)

        elif self.sys_config['model_parameters']['type'] == "pyspark":

            input_data = self.model_wrapper.read_data_to_spark(model_config=self.model_config,
                                                               file_schemas=input_schemas)

        else:
            raise ImportError('Parameter "Type" is defined incorrectly. Type can take values ["pandas", "pyspark"] and '
                              f'is currently set to {self.sys_config["model_parameters"]["type"]}.')

        return input_data

    def run_schema_conformance(self, data_dict: dict, schema_dict: dict) -> dict:
        data_errors = {}

        for key, val in data_dict.items():

            if self.sys_config['model_parameters']['type'] == "pandas":

                schema = InputOutputData.convert_schema_pandas(schema_dict[key])

                data_errors[key] = InputOutputData.schema_conformance_pandas(data=val, schema=schema, dataframe_name=key)

            elif self.sys_config['model_parameters']['type'] == "pandas":

                schema = InputOutputData.convert_schema_spark(schema_dict[key])

                data_errors[key] = InputOutputData.schema_conformance_spark(data=val, schema=schema, dataframe_name=key)

        return data_errors

    def create_data_dict(self):
        pass

    @staticmethod
    def read_config(path: str) -> dict:
        config_dict = InputOutputData.read_yaml(path=path)

        return config_dict
