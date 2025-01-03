import pandas as pd
import pytest

from framework.setup.read_data.schemas.format_schema import (
    ModelType, FormatPandasSchema, FormatSparkSchema, SchemaFormatFactory
)


def test_model_type_enum():
    assert ModelType.PANDAS.value == "pandas"
    assert ModelType.SPARK.value == "spark"


def test_format_pandas_schema():
    schema = {
        "id": "integer",
        "name": "string",
        "price": "float",
        "date": "date"
    }
    expected_schema = {
        "id": pd.Int64Dtype(),
        "name": "string",
        "price": pd.Float64Dtype(),
        "date": "datetime64[s]"
    }
    formatter = FormatPandasSchema()
    formatted_schema = formatter.format_schema(schema)
    assert formatted_schema == expected_schema


def test_format_spark_schema():
    schema = {
        "id": "integer",
        "name": "string",
        "price": "float",
        "date": "date"
    }
    formatter = FormatSparkSchema()
    formatted_schema = formatter.format_schema(schema)
    assert formatted_schema == schema  # Assuming no changes are made in the current implementation


def test_schema_format_factory_pandas():
    formatter = SchemaFormatFactory.get_schema_formatter(ModelType.PANDAS)
    assert isinstance(formatter, FormatPandasSchema)


def test_schema_format_factory_spark():
    formatter = SchemaFormatFactory.get_schema_formatter(ModelType.SPARK)
    assert isinstance(formatter, FormatSparkSchema)


def test_schema_format_factory_invalid_model_type():
    with pytest.raises(ValueError, match="Model type .* not supported."):
        SchemaFormatFactory.get_schema_formatter("invalid_model_type")
