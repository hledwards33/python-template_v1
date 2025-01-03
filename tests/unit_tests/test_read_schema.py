import json
from unittest.mock import patch, mock_open

import pytest
import yaml

from framework.setup.read_data.schemas.read_schema import (FileExtension, ReadJsonSchema, ReadYamlSchema, SchemaContext,
                                                           SchemaFactory)


def test_file_extension_enum():
    assert FileExtension.JSON.value == "json"
    assert FileExtension.YAML.value == "yaml"


def test_read_json_schema():
    schema_path = "test_schema.json"
    schema_data = {"name": "test"}
    with patch("builtins.open", mock_open(read_data=json.dumps(schema_data))):
        reader = ReadJsonSchema(schema_path)
        result = reader.read_schema()
        assert result == schema_data


def test_read_yaml_schema():
    schema_path = "test_schema.yaml"
    schema_data = {"name": "test"}
    with patch("builtins.open", mock_open(read_data=yaml.dump(schema_data))):
        reader = ReadYamlSchema(schema_path)
        result = reader.read_schema()
        assert result == schema_data


def test_schema_context():
    schema_path = "test_schema.json"
    context = SchemaContext(schema_path)
    assert context.schema_path == schema_path
    assert context.schema_extension == "json"


def test_schema_factory_create_json_reader():
    schema_path = "test_schema.json"
    context = SchemaContext(schema_path)
    reader = SchemaFactory.create_schema_reader(context)
    assert isinstance(reader, ReadJsonSchema)


def test_schema_factory_create_yaml_reader():
    schema_path = "test_schema.yaml"
    context = SchemaContext(schema_path)
    reader = SchemaFactory.create_schema_reader(context)
    assert isinstance(reader, ReadYamlSchema)


def test_schema_factory_invalid_extension():
    schema_path = "test_schema.txt"
    context = SchemaContext(schema_path)
    with pytest.raises(ValueError, match="Invalid schema file extension."):
        SchemaFactory.create_schema_reader(context)
