from abc import ABC, abstractmethod

from framework.data_scripts.read_inputs import InputData


class ModelWrapper(ABC):

    def __init__(self):
        pass

    @staticmethod
    def set_parameters():
        pass

    @staticmethod
    def read_schemas(schema_dict: dict) -> dict:

        schema_dict = {key: InputData.read_json(path=val) for key, val in schema_dict.items()}

        return schema_dict

    @staticmethod
    def read_data_to_pandas(model_config: dict, file_schemas: dict) -> dict:

        data_dict = {}

        for key, val in model_config['inputs']:

            file_type = val.split(".")[-1]

            if file_type in ["csv", "zip"]:

                data_dict[key] = InputData.read_csv_to_pandas(path=val, schema=file_schemas[key])

            elif file_type in ["pqt", "parquet"]:

                data_dict[key] = InputData.read_parquet_to_pandas(path=val, schema=file_schemas[key])

        return data_dict

    @staticmethod
    def read_data_to_spark(model_config: dict, file_schemas: dict) -> dict:
        # TODO: fill in the method
        pass

    @staticmethod
    def write_data_from_pandas(model_config: dict, file_schemas: dict):

        for key, val in model_config['inputs']:

            file_type = val.split(".")[-1]

            if file_type in ["csv", "zip"]:

                InputData.write_csv(path=val, schema=file_schemas[key])

            elif file_type in ["pqt", "parquet"]:

                InputData.write_parquet(path=val, schema=file_schemas[key])

    @staticmethod
    def write_data_from_spark(path: str, file_schemas: dict):
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

    def post_outputs(self, data: dict):
        if self.sys_config['model_parameters']['type'] == "pandas":
            output_schemas = self.model_wrapper.read_schemas(schema_dict=self.model_wrapper.define_input_schemas())



        elif self.sys_config['model_parameters']['type'] == "pyspark":
            input_schemas = self.model_wrapper.read_schemas(schema_dict=self.model_wrapper.define_input_schemas())

    def get_inputs(self) -> dict:
        if self.sys_config['model_parameters']['type'] == "pandas":
            input_schemas = self.model_wrapper.read_schemas(schema_dict=self.model_wrapper.define_input_schemas())

            input_schemas = InputData.convert_schema_pandas(schema=input_schemas)

            input_data = self.model_wrapper.read_data_to_pandas(model_config=self.model_config,
                                                                file_schemas=input_schemas)

        elif self.sys_config['model_parameters']['type'] == "pyspark":
            input_schemas = self.model_wrapper.read_schemas(schema_dict=self.model_wrapper.define_input_schemas())

            input_schemas = InputData.convert_schema_spark(schema=input_schemas)

            input_data = self.model_wrapper.read_data_to_spark(model_config=self.model_config,
                                                               file_schemas=input_schemas)

        else:
            raise ImportError('Parameter "Type" is defined incorrectly. Type can take values ["pandas", "pyspark"] and '
                              f'is currently set to {self.sys_config["model_parameters"]["type"]}.')

        return input_data

    def create_data_dict(self):
        pass

    @staticmethod
    def read_config(path: str) -> dict:
        config_dict = InputData.read_yaml(path=path)

        return config_dict
