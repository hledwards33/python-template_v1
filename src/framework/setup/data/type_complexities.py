from enum import Enum


class ModelType(Enum):
    PANDAS = "pandas"
    SPARK = "spark"

class SchemaExtension(Enum):
    JSON = "json"
    YAML = "yaml"
    YAML_SHORT = "yml"

class FileExtension(Enum):
    CSV = "csv"
    ZIP = "zip"
    PARQUET = "parquet"
    PQT = "pqt"
