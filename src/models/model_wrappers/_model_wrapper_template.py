# TODO: See example_model.py for reference.
from framework.model_wrapper import ModelWrapper, DeployWrapper
# TODO: Amend the below import statements to desired models schemas and model code.
from models import model_schemas as parameter_schemas
from models.model_schemas import example_model as model_schemas
from models.model_scripts.example_model.example_model import ExampleModel as Model


class ExampleModelWrapper(ModelWrapper):

    def __init__(self):
        super().__init__()

    # TODO: Option 1: If a parameter file is defined in the model config use this method and delete option 2.
    def define_parameter_schemas(self) -> tuple:
        return parameter_schemas, "parameters_schema.json"

    # TODO: Option 2: If no parameter file is defined in the model config use this method and delete option 1.
    def define_parameter_schemas(self) -> tuple:
        return parameter_schemas, "parameters_schema.json"


    def define_input_schemas(self) -> dict:
        return {
            'pd_data': (model_schemas, "pd_data_schema.json"),
            'lgd_data': (model_schemas, "lgd_data_schema.json"),
            'ead_data': (model_schemas, "ead_data_schema.json"),
        }

    def define_output_schemas(self) -> dict:
        return {
            'ecl_data': (model_schemas, "ecl_data_schema.json")
        }

    def run_model(self) -> dict:
        model_result = Model(input_data=self.data_dict, parameters=self.parameters).run()

        return model_result


if __name__ == "__main__":
    wrapper = DeployWrapper(model_wrapper=ExampleModelWrapper, sys_config='config/system_config.yml',
                            model_config='config/model_config/example_model/example_model_parquet_files_config.yml')

    wrapper.run_model()
# TODO: Delete all TODO comments once and format file.
