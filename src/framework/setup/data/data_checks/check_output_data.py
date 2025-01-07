import logging
from abc import ABC, abstractmethod

import pandas as pd

from framework.setup.data.type_complexities import ModelType

logger = logging.getLogger()


class IDataCheck(ABC):

    def __init__(self, data):
        self.data = data

    @abstractmethod
    def check_data(self, schema, dataframe_name):
        pass


class PandasDataCheck(IDataCheck):
    def __init__(self, data: pd.DataFrame):
        super().__init__(data)

    def check_data(self, schema: dict, dataframe_name: str = "") -> dict:
        # Create a holding variable to store any found errors
        errors = {'incorrect_type': []}

        # Check for column differences between schema and dataset
        extra_cols = list(set(self.data.columns).difference(schema.keys()))
        if extra_cols:
            # The below message is executed again in the "write_csv_from_pandas" method
            self.data.drop(columns=extra_cols, inplace=True)
            logger.warning(f"The following columns have been dropped from dataset {dataframe_name}: {extra_cols}.")

        # Check for columns in the schemas which are missing from the dataset
        missing_cols = set(schema.keys()).difference(self.data.columns)
        if len(missing_cols) > 0:
            errors['missing_columns'] = [f"Dataframe {dataframe_name} is missing the following columns {missing_cols}."]

        # Check the datatypes in the dataframe match those defined in the schema
        for col in self.data.columns:
            # Log a successful match if the datatypes are the same
            if str(self.data[col].dtype).lower() == str(schema[col]).lower():
                logger.info(f"Dataset {dataframe_name} has {col} with correct type: {self.data[col].dtype}.")

            # Save to error dictionary if the datatypes don't match
            else:
                errors['incorrect_type'] += [f"Dataframe {dataframe_name} has incorrect datatype in {col} "
                                             f"expected {schema[col]} got {self.data[col].dtype}."]

        # Return a dictionary of errors between the schema and dataframe
        return errors


class SparkDataCheck(IDataCheck):
    def check_data(self, schema, dataframe_name):
        # TODO: Implement this method
        pass

class DataCheckContext:
    def __init__(self, data, model_type: str):
        self.data = data
        self.model_type = model_type

class DataCheckFactory:
    @staticmethod
    def get_data_checker(model_type: str) -> IDataCheck:
        match model_type:
            case ModelType.PANDAS.value:
                return PandasDataCheck()
            case ModelType.SPARK.value:
                return SparkDataCheck()
            case _:
                raise ValueError("Invalid model type")
