from enum import Enum
from abc import ABC, abstractmethod

class ModelType(Enum):
    PANDAS = "pandas"
    SPARK = "spark"

class IFormatSchema(ABC):
    def __init__(self, schema_path: str):
        """
        Initializes the schema reader with the given schema path.

        Args:
            schema_path (str): Path to the schema file.
        """
        self.schema_path = schema_path

    @abstractmethod
    def format_schema(self) -> dict:
        """
        Reads the schema from the file.

        Returns:
            dict: Dictionary containing the schema data.
        """
        pass