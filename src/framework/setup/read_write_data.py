import json
import logging
import os

import numpy as np
import pandas as pd
import yaml

logger = logging.getLogger()


def read_json(path: tuple) -> dict:
    path = os.path.join(os.path.dirname(path[0].__file__), path[1])

    with open(path, 'r') as file:
        result = json.load(file)

    return result


def read_json_abs(path: str) -> dict:
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
            schema[key] = pd.Int64Dtype()
        elif val.lower() == 'float':
            schema[key] = pd.Float64Dtype()
        elif val.lower() == 'date':
            schema[key] = 'datetime64[s]'
        elif val.lower() == 'string':
            schema[key] = 'string'

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
            schema[key] = 'string'

    return schema


def convert_schema_recon_pandas(schema: dict) -> dict:
    for key, val in schema.items():
        if val.lower() == 'integer':
            schema[key] = pd.Int64Dtype()
        elif val.lower() == 'float':
            schema[key] = pd.Float64Dtype()
        elif val.lower() == 'date':
            schema[key] = 'string'
        elif val.lower() == 'string':
            schema[key] = 'string'

    return schema


def convert_schema_spark(schema: dict) -> dict:
    pass


def enforce_integers(df: pd.DataFrame) -> pd.DataFrame:
    for column in df.columns:
        if df[column].dtype == "Int64" and df[column].isna().all():
            df[column] = np.nan
        elif df[column].dtype == "Int64" and df[column].isna().any():
            df[column] = df[column].astype(np.float64)
        elif df[column].dtype == "Int64":
            df[column] = df[column].astype(np.int64)

    return df


def enforce_floats(df: pd.DataFrame) -> pd.DataFrame:
    for column in df.columns:
        if df[column].dtype == "Float64":
            df[column] = df[column].astype(np.float64)
    return df


def enforce_strings(df: pd.DataFrame) -> pd.DataFrame:
    for column in df.columns:
        if df[column].dtype in ["string", "object"]:
            df[column] = df[column].mask(df[column] == "")
            df[column] = df[column].mask(df[column].str.lower() == "nan")
    return df


def enforce_data_types(df: pd.DataFrame) -> pd.DataFrame:
    df = enforce_integers(df)
    df = enforce_floats(df)
    df = enforce_strings(df)
    return df


def schema_conformance_spark(data: pd.DataFrame, schema: dict, dataframe_name: str = "") -> dict:
    pass


def schema_conformance_pandas(data: pd.DataFrame, schema: dict, dataframe_name: str = "") -> dict:
    errors = {'incorrect_type': []}

    extra_cols = list(set(data.columns).difference(schema.keys()))
    if extra_cols:
        data.drop(columns=extra_cols, inplace=True)
        logger.warning(f"The following columns have been dropped from dataset {dataframe_name}: {extra_cols}")

    missing_cols = set(schema.keys()).difference(data.columns)
    if len(missing_cols) > 0:
        errors['missing_columns'] = [f"Dataframe {dataframe_name} is missing the following columns {missing_cols}."]

    for col in data.columns:
        if str(data[col].dtype).lower() == schema[col].lower():
            logger.info(f"Dataset {dataframe_name} has {col} with correct type: {data[col].dtype}.")

        else:
            errors['incorrect_type'] += [f"Dataframe {dataframe_name} has incorrect datatype in {col} "
                                         f"expected {schema[col]} got {data[col].dtype}."]

    return errors


def read_csv_to_pandas(path: str, schema: dict, usecols: bool = True) -> pd.DataFrame:
    logger.info(f"Loading columns: {list(schema.keys())}")

    kwargs = {
        'filepath_or_buffer': path,
        'dtype': schema,
        'usecols': schema.keys(),
        'cache_dates': True,
        'engine': 'pyarrow',
        'parse_dates': [key for key, val in schema.items() if val == 'datetime64[s]'],
        'date_format': "%Y-%m-%d",
    }

    if not usecols:
        del kwargs['usecols']

    data = pd.read_csv(**kwargs)

    data = enforce_data_types(data)

    return data


def read_parquet_to_pandas(path: str, schema: dict, usecols: bool = True) -> pd.DataFrame:
    logger.info(f"Loading columns: {list(schema.keys())}")

    # Parquet files store dtypes in metadata so schema is not required when reading
    kwargs = {
        'path': path,
        'columns': schema.keys(),
        'engine': 'pyarrow',
        'dtype_backend': 'numpy_nullable'
    }

    if not usecols:
        del kwargs['columns']

    data = pd.read_parquet(**kwargs)

    # Add datatypes from schema in case parquet file was created incorrectly
    for column in data.columns:
        data[column] = data[column].astype(schema[column])

    data = enforce_data_types(data)

    return data


def read_csv_to_spark(path: str, schema: dict) -> pd.DataFrame:
    # TODO: Fill in this method
    pass


def read_parquet_to_spark(path: str, schema: dict) -> pd.DataFrame:
    # TODO: Fill in this method
    pass


def write_csv_from_pandas(data: pd.DataFrame, path: str, schema: dict, dataframe_name: str = ""):
    kwargs = {'path_or_buf': path, 'na_rep': "", 'columns': schema.keys(), 'index': False}

    data.to_csv(**kwargs)


def write_parquet_from_pandas(data: pd.DataFrame, path: str, schema: dict):
    kwargs = {'path': path, 'partition_cols': schema.keys(), 'index': False, 'engine': 'pyarrow', 'compression': 'gzip'}

    data.to_parquet(**kwargs)


def write_zip_from_pandas(data: pd.DataFrame, path: str, schema: dict):
    kwargs = {'path_or_buf': path, 'na_rep': "", 'columns': schema.keys(), 'index': False,
              'compression': {'method': 'zip'}}

    data.to_csv(**kwargs)


def write_csv_from_spark(data: pd.DataFrame, path: str, schema: dict, dataframe_name: str = ""):
    # TODO: Fill in this method
    pass


def write_parquet_from_spark(data: pd.DataFrame, path: str, schema: dict):
    # TODO: Fill in this method
    pass


def write_zip_from_spark(ata: pd.DataFrame, path: str, schema: dict):
    # TODO: Fill in this method
    pass
