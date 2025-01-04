from framework.setup.create_model.build_model import ModelMetaData, ModelBuilder, ModelDirector
from framework.setup.create_model.model_wrapper import ModelWrapper
from framework.setup.read_data.read_data import DataContext, DataBuilder, DataDirector


class Model:
    def __init__(self):
        self._model_inputs = dict()
        self._model_outputs = dict()
        self._model_parameters = dict()

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
    def __init__(self, model_wrapper: ModelWrapper, model_config_path: str):
        self._model_metadata: ModelMetaData = self.create_model_metadata(model_wrapper, model_config_path)

        self._model = None

    def create_model(self):
        self._model = Model()

    def get_model(self):
        return self._model

    @staticmethod
    def create_model_metadata(model_wrapper: ModelWrapper, model_config_path: str) -> ModelMetaData:
        model_builder = ModelBuilder(model_wrapper, model_config_path)
        return ModelDirector(model_builder).build_model()

    def read_input(self, data_paths):
        data_path, schema_path = data_paths
        input_data_context = DataContext(schema_path, data_path, self._model_metadata.model_type)
        input_data_builder = DataBuilder(input_data_context)
        input_data, errors = DataDirector(input_data_builder).read_data()
        return input_data, errors

    def read_input_data(self):
        errors = {}
        for data_name, data_paths in self._model_metadata.model_inputs.items():
            input_data, errors = self.read_input(data_paths)
            self._model.model_inputs[data_name] = input_data
            errors[data_name] = errors

        if errors:
            # TODO: Add logging of errors
            raise ValueError("Errors occurred when reading input data, see the above logs.")

    def run_model(self):
        pass


class DeployModelDirector:
    pass


class DeployModel:
    pass