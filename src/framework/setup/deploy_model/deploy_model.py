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

    def run_model(self):
        self._model_metadata.run_model(self._model.model_inputs, self._model.model_parameters)

    def read_parameters(self):
        self._model.model_parameters = self._model_metadata.model_parameters

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

    def write_output_data(self):
        pass


class DeployModelDirector:
    def __init__(self, builder: DeployModelBuilder):
        self.builder = builder

    def build_model_deployment(self):
        self.builder.create_model()
        self.builder.read_parameters()
        self.builder.read_input_data()
        self.builder.run_model()
        self.builder.write_output_data()


class DeployModel:

    def __init__(self, model_wrapper: ModelWrapper, model_config_path: str):
        self.model_wrapper = model_wrapper
        self.model_config_path = model_config_path

    def deploy(self):
        model_builder = DeployModelBuilder(self.model_wrapper, self.model_config_path)
        DeployModelDirector(model_builder).build_model_deployment()


if __name__ == "__main__":
    pass
