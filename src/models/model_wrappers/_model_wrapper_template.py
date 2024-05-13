# TODO: To use this template copy and rename this file.
# TODO: See example_model.py for reference.
from framework.model_wrapper import ModelWrapper, DeployWrapper

# TODO: Delete below import statement if a parameter input file is not defined in the model config yaml.
from models import model_schemas as parameter_schemas

# TODO: Amend the below import statements (see capitalised parts) to desired models references.
from models.model_schemas import YOUR_MODEL_SCHEMAS as model_schemas
from models.model_scripts.YOUR_MODEL_DIR.YOUR_MODEL_SCRIPT import YOUR_MODEL_CLASS as Model


# TODO: Rename the "TemplateWrapper" to: model name + "Wrapper", using CamelCase.
class TemplateWrapper(ModelWrapper):

    def __init__(self):
        super().__init__()

    # TODO: Select the appropriate define_parameter_schemas method from the options below.
    # TODO: Option 1: If a parameter input file is defined in the model config use this method and delete option 2.
    def define_parameter_schemas(self) -> tuple:
        return parameter_schemas, "parameters_schema.json"

    # TODO: Option 2: If no parameter input file is defined in the model config use this method and delete option 1.
    def define_parameter_schemas(self) -> tuple:
        return parameter_schemas, "parameters_schema.json"

    def define_input_schemas(self) -> dict:
        # TODO: define all input datasets and schemas in the dictionary below, using "data" as a syntax reference.
        return {
            'data': (model_schemas, "data_schema.json"),  # TODO: Delete "data" entry once no longer needed.
        }

    def define_output_schemas(self) -> dict:
        # TODO: define all output datasets and schemas in the dictionary below, using "data" as a syntax reference.
        return {
            'data': (model_schemas, "data_schema.json"),  # TODO: Delete "data" entry once no longer needed.
        }

    def run_model(self) -> dict:
        model_result = Model(input_data=self.data_dict, parameters=self.parameters).run()

        return model_result


if __name__ == "__main__":
    # TODO: Rename "TemplateWrapper" to match the wrapper class name above.
    wrapper = DeployWrapper(model_wrapper=TemplateWrapper, sys_config='config/system_config.yml',
                            model_config='config/model_config/example_model/example_model_parquet_files_config.yml')

    wrapper.run_model()
# TODO: Delete all TODO comments and format file.
