import json
import os

import pandas as pd
import yaml

import logging

logger = logging.getLogger()


def read_json(path: str) -> dict:
    path = os.path.join(os.path.dirname(path[0].__file__), path[1])

    with open(path, 'r') as file:
        result = json.load(file)

    return result


def read_yaml(path: str) -> dict:
    with open(path, 'r') as file:
        result = yaml.safe_load(file)

    return result


def convert_schema_pandas(schema: dict) -> dict:
    for key, val in schema.items():
        if val.lower() == 'integer':
            schema[key] = 'Int64'
        elif val.lower() == 'float':
            schema[key] = 'Float64'
        elif val.lower() == 'date':
            schema[key] = 'datetime64[s]'
        elif val.lower() == 'string':
            schema[key] = 'object'

    return schema


def convert_schema_output_pandas(schema: dict) -> dict:
    for key, val in schema.items():
        if val.lower() == 'integer':
            schema[key] = 'Int64'
        elif val.lower() == 'float':
            schema[key] = 'Float64'
        elif val.lower() == 'date':
            schema[key] = 'datetime64[s]'
        elif val.lower() == 'string':
            schema[key] = 'object'

    return schema


def convert_schema_spark(schema: dict) -> dict:
    pass


def schema_conformance_spark(data: pd.DataFrame, schema: dict, dataframe_name: str = "") -> dict:
    pass


def schema_conformance_pandas(data: pd.DataFrame, schema: dict, dataframe_name: str = "") -> dict:
    errors = {'incorrect_type': []}

    extra_cols = set(data.columns).difference(schema.keys())
    # TODO: Log: extra columns... have been dropped

    missing_cols = set(schema.keys()).difference(data.columns)
    if len(missing_cols) > 0:
        errors['missing_columns'] = [f"Dataframe {dataframe_name} is missing the following columns {missing_cols}."]

    for col in data.columns:
        if data[col].dtype == schema[col]:
            logger.info(f"Dataset {dataframe_name} has {col} with correct type: {data[col].dtype}.")

        else:
            errors['incorrect_type'] += [f"Dataframe {dataframe_name} has incorrect datatype in {col} "
                                         f"expected {schema[col]} got {data[col].dtype}."]

    return errors


def read_csv_to_pandas(path: str, schema: dict) -> pd.DataFrame:
    # TODO: Log dataset x is being read in, only columns defined in schemas are read
    # TODO: Check if this works with zip files and add if_zip to the read data func
    kwargs = {
        'filepath_or_buffer': path,
        'dtype': schema,
        'usecols': schema.keys(),
        'cache_dates': True,
        'engine': 'pyarrow',
        'parse_dates': [key for key, val in schema.items() if val == "date"],
        'date_format': "%Y-%m-%d"
    }

    data = pd.read_csv(**kwargs)

    return data


def read_parquet_to_pandas(path: str, schema: dict) -> pd.DataFrame:
    # TODO: Fill in this method
    pass


def read_csv_to_spark(path: str, schema: dict) -> pd.DataFrame:
    # TODO: Fill in this method
    pass


def read_parquet_to_spark(path: str, schema: dict) -> pd.DataFrame:
    # TODO: Fill in this method
    pass


def write_csv_from_pandas(data: pd.DataFrame, path: str, schema: dict, dataframe_name: str = ""):
    kwargs = {'path': path, 'na_rep': "", 'columns': schema.keys(), 'index': False}

    data.to_csv(**kwargs)


def write_parquet_from_pandas(data: pd.DataFrame, path: str, schema: dict):
    # TODO: Fill in this method
    pass


def write_zip_from_pandas(data: pd.DataFrame, path: str, schema: dict):
    # TODO: Fill in this method
    pass


def write_csv_from_spark(data: pd.DataFrame, path: str, schema: dict, dataframe_name: str = ""):
    # TODO: Fill in this method
    pass


def write_parquet_from_spark(data: pd.DataFrame, path: str, schema: dict):
    # TODO: Fill in this method
    pass


def write_zip_from_spark(ata: pd.DataFrame, path: str, schema: dict):
    # TODO: Fill in this method
    pass
