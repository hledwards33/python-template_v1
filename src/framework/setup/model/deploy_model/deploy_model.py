from framework.setup.data.read_data.read_data import ReadDataContext, ReadDataBuilder, ReadDataDirector
from framework.setup.data.write_data.write_data import WriteDataContext, WriteDataBuilder, WriteDataDirector
from framework.setup.logs.log_builders import LogBuilder
from framework.setup.logs.log_handlers import LogHandlerContext, LogHandlerFactory
from framework.setup.logs.log_structures import LogStructures
from framework.setup.model.create_model.build_model import ModelMetaData, ModelBuilder, ModelDirector
from framework.setup.model.create_model.model_wrapper import IModelWrapper


class Model:

    def __init__(self):
        self._model_inputs = dict()
        self._model_outputs = dict()
        self._model_parameters = dict()
        self._logging = "HERE"

    @property
    def logging(self):
        return self._logging

    @logging.setter
    def logging(self, value):
        self._logging = value

    @property
    def model_inputs(self):
        return self._model_inputs

    @model_inputs.setter
    def model_inputs(self, value):
        self._model_inputs = value

    @property
    def model_outputs(self):
        return self._model_outputs

    @model_outputs.setter
    def model_outputs(self, value):
        self._model_outputs = value

    @property
    def model_parameters(self):
        return self._model_parameters

    @model_parameters.setter
    def model_parameters(self, value):
        self._model_parameters = value


class DeployModelBuilder:
    def __init__(self, model_wrapper: IModelWrapper, model_config_path: str):
        self._model_metadata: ModelMetaData = self.create_model_metadata(model_wrapper, model_config_path)

        self._model = None

    def create_model(self):
        self._model = Model()

    def get_model(self):
        return self._model

    def initiate_logging(self):
        log_context = LogHandlerContext(self._model_metadata.log_file_path, self._model_metadata.log_format)
        sys_handler, file_handler = LogHandlerFactory(log_context).create_handlers()
        logger = LogBuilder(sys_handler, file_handler)
        logger.initiate_logging()
        # TODO: consider how to make this global so it can be accessed by all scripts
        self._model.logging = LogStructures(self._model_metadata.log_format)

    @staticmethod
    def create_model_metadata(model_wrapper: IModelWrapper, model_config_path: str) -> ModelMetaData:
        model_builder = ModelBuilder(model_wrapper, model_config_path)
        return ModelDirector(model_builder).build_model()

    def run_model(self):
        self._model.model_outputs = self._model_metadata.model(self._model.model_inputs,
                                                               self._model.model_parameters).run()

    def read_parameters(self):
        # TODO: write a method that unpacks the parameters and model types
        pass

    def read_input(self, data_paths):
        data_path, schema_path = data_paths
        input_data_context = ReadDataContext(schema_path, data_path,
                                             self._model_metadata.model_type)
        input_data_builder = ReadDataBuilder(input_data_context)
        input_data, errors = ReadDataDirector(input_data_builder).read_data()
        return input_data, errors

    def read_input_data(self):
        all_errors = {}
        for data_name, data_paths in self._model_metadata.model_inputs.items():
            input_data, errors = self.read_input(data_paths)
            self._model.model_inputs[data_name] = input_data
            if not errors: all_errors[data_name] = errors

        if all_errors:
            # TODO: Add logging of errors
            raise ValueError("Errors occurred when reading input data, see the above logs.")

    def write_output(self, data, data_paths):
        data_path, schema_path = data_paths
        output_data_context = WriteDataContext(data, schema_path, data_path,
                                               self._model_metadata.model_type)
        output_data_builder = WriteDataBuilder(output_data_context)
        return WriteDataDirector(output_data_builder).write_data()

    def write_output_data(self):
        all_errors = {}
        for data_name, data_paths in self._model_metadata.model_outputs.items():
            data = self._model.model_outputs[data_name]
            errors = self.write_output(data, data_paths)
            if not errors: all_errors[data_name] = errors

        if all_errors:
            # TODO: Add logging of errors
            raise ValueError("Errors occurred when reading input data, see the above logs.")


class DeployModelDirector:
    def __init__(self, builder: DeployModelBuilder):
        self.builder = builder

    def build_model_deployment(self):
        self.builder.create_model()
        self.builder.initiate_logging()
        self.builder.read_parameters()
        self.builder.read_input_data()
        self.builder.run_model()
        self.builder.write_output_data()


class DeployModel:

    def __init__(self, model_wrapper: IModelWrapper, model_config_path: str):
        self.model_wrapper = model_wrapper
        self.model_config_path = model_config_path

    def deploy(self):
        model_builder = DeployModelBuilder(self.model_wrapper, self.model_config_path)
        DeployModelDirector(model_builder).build_model_deployment()


if __name__ == "__main__":
    from framework.setup.model.deploy_model.TEMP_example_model_wrapper import ExampleModelWrapper

    DeployModel(model_wrapper=ExampleModelWrapper(),
                model_config_path='config/model_config/example_model/example_model_config.yml').deploy()
