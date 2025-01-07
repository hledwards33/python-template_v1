from framework.setup.model.create_model.model_wrapper import IModelWrapper
from models.model_schemas import example_model as model_schemas

from framework.setup.model.create_model.TEMP_example_model import ExampleModel as Model


class ExampleModelWrapper(IModelWrapper):
    def define_parameters(self) -> dict:
        return {"ecl_lower_limit": self.parameter_types.FLOAT,
                "ecl_upper_limit": self.parameter_types.INTEGER}

    def define_inputs(self) -> dict:
        return {
            'pd_data': (model_schemas, "pd_data_schema.json"),
            'lgd_data': (model_schemas, "lgd_data_schema.json"),
            'ead_data': (model_schemas, "ead_data_schema.json"),
        }

    def define_outputs(self) -> dict:
        return {
            'ecl_data': (model_schemas, "ecl_data_schema.json")
        }

    def define_model(self):
        return Model
