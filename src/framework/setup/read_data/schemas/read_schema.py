import json
from abc import ABC, abstractmethod
from enum import Enum

import yaml


class FileExtension(Enum):
    JSON = "json"
    YAML = "yaml"


class IReadSchema(ABC):
    def __init__(self, schema_path: str):
        """
        Initializes the schema reader with the given schema path.

        Args:
            schema_path (str): Path to the schema file.
        """
        self.schema_path = schema_path

    @abstractmethod
    def read_schema(self) -> dict:
        """
        Reads the schema from the file.

        Returns:
            dict: Dictionary containing the schema data.
        """
        pass


class ReadJsonSchema(IReadSchema):
    def read_schema(self) -> dict:
        """
        Reads the schema from a JSON file.

        Returns:
            dict: Dictionary containing the JSON schema data.
        """
        with open(self.schema_path, 'r') as file:
            result = json.load(file)
        return result


class ReadYamlSchema(IReadSchema):
    def read_schema(self) -> dict:
        """
        Reads the schema from a YAML file.

        Returns:
            dict: Dictionary containing the YAML schema data.
        """
        with open(self.schema_path, 'r') as file:
            result = yaml.safe_load(file)
        return result


class SchemaContext:
    def __init__(self, schema_path: str):
        """
        Initializes the schema context with the given schema path.

        Args:
            schema_path (str): Path to the schema file.
        """
        self.schema_path = schema_path
        self.schema_extension = schema_path.split(".")[-1].lower()


class SchemaFactory:
    @staticmethod
    def create_schema_reader(context: SchemaContext) -> IReadSchema:
        """
        Creates a schema reader based on the file extension.

        Args:
            context (SchemaContext): Context containing the schema path and extension.

        Returns:
            IReadSchema: An instance of a schema reader.
        
        Raises:
            ValueError: If the schema file extension is invalid.
        """
        match context.schema_extension:
            case FileExtension.JSON.value:
                return ReadJsonSchema(context.schema_path)
            case FileExtension.YAML.value:
                return ReadYamlSchema(context.schema_path)
            case _:
                raise ValueError(f"Invalid schema file extension: {context.schema_extension}.")
