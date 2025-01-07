from abc import ABC, abstractmethod

import pandas as pd

from framework.setup.data.type_complexities import ModelType


class IFormatSchema(ABC):

    @abstractmethod
    def format_schema(self, schema: dict) -> dict:
        """
        Formats the schema data.

        Returns:
            dict: Dictionary containing the formatted schema data.
        """
        pass


class FormatPandasSchema(IFormatSchema):
    def format_schema(self, schema: dict) -> dict:
        """
        Takes a standardised data schema and returns it in a Pandas compatible format. Converts schema values into
        values that are compatible with pandas.read_csv().

        Returns:
            dict: Dictionary containing the schema data in a Pandas format.
        """
        # Loop through each datatype and standardise to conform with pandas
        for key, val in schema.items():
            if val.lower() == 'integer':
                schema[key] = pd.Int64Dtype()
            elif val.lower() == 'float':
                schema[key] = pd.Float64Dtype()
            elif val.lower() == 'date':
                schema[key] = 'datetime64[s]'
            elif val.lower() == 'string':
                schema[key] = 'string'

        # Return the updated schema dictionary
        return schema


class FormatSparkSchema(IFormatSchema):
    def format_schema(self, schema: dict) -> dict:
        """
        Takes a standardised data schema and returns it in a Spark compatible format.

        Returns:
            dict: Dictionary containing the schema data in a Spark format.
        """
        # TODO: Implement the conversion logic. And write unit tests for this method.
        return schema


class SchemaFormatFactory:
    @staticmethod
    def get_schema_formatter(model_type: str) -> IFormatSchema:
        """
        Factory method that returns the appropriate schema formatter based on the model type.

        Args:
            model_type (ModelType): the type of model to format the schema for.
            schema (dict): the schema to format.

        Returns:
            IFormatSchema: The schema formatter.
        """
        match model_type:
            case ModelType.PANDAS.value:
                return FormatPandasSchema()
            case ModelType.SPARK.value:
                return FormatSparkSchema()
            case _:
                raise ValueError(f"Model type {model_type} not supported.")
