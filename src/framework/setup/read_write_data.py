import json
import logging
import os

import numpy as np
import pandas as pd
import yaml

logger = logging.getLogger()


def read_json(path: tuple) -> dict:
    """
    Loads a json file into a dictionary object
    :param path: tuple containing imported module and file name
    :return: dictionary containing json file's content
    """

    # Create a string path from the passed arguments
    path = os.path.join(os.path.dirname(path[0].__file__), path[1])

    # Open the json file and load to a dictionary
    with open(path, 'r') as file:
        result = json.load(file)

    # Return json file content within a dictionary object
    return result


def read_json_abs(path: str) -> dict:
    """
    Loads a json file into a dictionary object
    :param path: string pointing to a json file
    :return: dictionary containing json file's content
    """
    # Open the json file and load to a dictionary
    with open(path, 'r') as file:
        result = json.load(file)

    # Return json file content within a dictionary object
    return result


def read_yaml(path: str) -> dict:
    """
    Loads a yaml file into a dictionary object
    :param path: string pointing to a yaml file
    :return: dictionary containing yaml file's content
    """
    # Open the yaml file and load to a dictionary
    with open(path, 'r') as file:
        result = yaml.safe_load(file)

    # Return yaml file content within a dictionary object
    return result


def convert_schema_pandas(schema: dict) -> dict:
    """
    Converts schema values into values that are compatible with pandas.read_csv()
    :param schema: dictionary containing columns and datatypes
    :return: dictionary containing columns and standardised datatypes
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


def convert_schema_output_pandas(schema: dict) -> dict:
    """
    Converts schema values into values that are compatible with pandas.to_csv()
    :param schema: dictionary containing columns and datatypes
    :return: dictionary containing columns and standardised datatypes
    """
    # Loop through each datatype and standardise to conform with pandas
    for key, val in schema.items():
        if val.lower() == 'integer':
            schema[key] = 'Int64'
        elif val.lower() == 'float':
            schema[key] = 'Float64'
        elif val.lower() == 'date':
            schema[key] = 'datetime64[s]'
        elif val.lower() == 'string':
            schema[key] = 'string'

    # Return the updated schema dictionary
    return schema


def convert_schema_recon_pandas(schema: dict) -> dict:
    """
    Converts schema values into values that are compatible with pandas.to_csv()
    :param schema: dictionary containing columns and datatypes
    :return: dictionary containing columns and standardised datatypes
    """
    # Loop through each datatype and standardise to conform with pandas
    for key, val in schema.items():
        if val.lower() == 'integer':
            schema[key] = pd.Int64Dtype()
        elif val.lower() == 'float':
            schema[key] = pd.Float64Dtype()
        elif val.lower() == 'date':
            schema[key] = 'string'
        elif val.lower() == 'string':
            schema[key] = 'string'

    # Return the updated schema dictionary
    return schema


def convert_schema_spark(schema: dict) -> dict:
    # TODO: Fill in this method
    pass


def enforce_integers(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardises the integer fields in any given dataframe
    :param df: pandas dataframe object
    :return: pandas dataframe with standardised integer fields
    """

    # Loop through each column and standardise integer fields
    for column in df.columns:
        if df[column].dtype == "Int64" and df[column].isna().all():
            df[column] = pd.NA
            df[column] = df[column].astype('Int64')
        elif df[column].dtype == "Int64" and df[column].isna().any():
            df[column] = df[column].astype('Int64')
        elif df[column].dtype == "Int64":
            df[column] = df[column].astype('Int64')

    # Return a dataframe with standardised integer fields
    return df


def enforce_floats(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardises the float fields in any given dataframe
    :param df: pandas dataframe object
    :return: pandas dataframe with standardised float fields
    """
    # Loop through each column and standardise float fields
    for column in df.columns:
        if df[column].dtype == "Float64":
            df[column] = df[column].astype(np.float64)

    # Return a dataframe with standardised float fields
    return df


def enforce_strings(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardises the string fields in any given dataframe
    :param df: pandas dataframe object
    :return: pandas dataframe with standardised string fields
    """
    # Loop through each column and standardise string fields
    for column in df.columns:
        if df[column].dtype in ["string", "object"]:
            df[column] = df[column].mask(df[column] == "")
            df[column] = df[column].mask(df[column].str.lower() == "nan")

    # Return a dataframe with standardised string fields
    return df


def enforce_data_types(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardises the values in each column of the passed dataset
    :param df: pandas dataset object
    :return: pandas dataset with standardised values
    """
    # Standardise integer values
    df = enforce_integers(df)

    # Standardise float values
    df = enforce_floats(df)

    # Standardise string values
    df = enforce_strings(df)

    # Return a dataframe with standardised values
    return df


def schema_conformance_spark(data: pd.DataFrame, schema: dict, dataframe_name: str = "") -> dict:
    # TODO: Fill in this method
    pass


def schema_conformance_pandas(data: pd.DataFrame, schema: dict, dataframe_name: str = "") -> dict:
    """
    Checks that the passed dataset has datatypes matching the passed schema
    :param data: pandas dataframe
    :param schema: dictionary containing column names as keys and datatypes as values
    :param dataframe_name: Name of the dataset
    :return: errors in dataframe-schema conformance if any
    """
    # Create a holding variable to store any found errors
    errors = {'incorrect_type': []}

    # Check for column differences between schema and dataset
    extra_cols = list(set(data.columns).difference(schema.keys()))
    if extra_cols:
        # The below message is executed again in the "write_csv_from_pandas" method
        data.drop(columns=extra_cols, inplace=True)
        logger.warning(f"The following columns have been dropped from dataset {dataframe_name}: {extra_cols}.")

    # Check for columns in the schemas which are missing from the dataset
    missing_cols = set(schema.keys()).difference(data.columns)
    if len(missing_cols) > 0:
        errors['missing_columns'] = [f"Dataframe {dataframe_name} is missing the following columns {missing_cols}."]

    # Check the datatypes in the dataframe match those defined in the schema
    for col in data.columns:
        # Log a successful match if the datatypes are the same
        if str(data[col].dtype).lower() == schema[col].lower():
            logger.info(f"Dataset {dataframe_name} has {col} with correct type: {data[col].dtype}.")

        # Save to error dictionary if the datatypes do not match
        else:
            errors['incorrect_type'] += [f"Dataframe {dataframe_name} has incorrect datatype in {col} "
                                         f"expected {schema[col]} got {data[col].dtype}."]

    # Return a dictionary of errors between the schema and dataframe
    return errors


def read_csv_to_pandas(path: str, schema: dict, usecols: bool = True) -> pd.DataFrame:
    """
    Loads a csv or zipped csv into a pandas dataframe object
    :param path: path to csv
    :param schema: dictionary containing column datatypes
    :param usecols: Boolean to choose only loading columns defined in the schema
    :return: pandas dataframe object containing the csv data
    """
    logger.info(f"Loading columns: {list(schema.keys())}")

    # Define the key word arguments to be supplied to the pandas.read_csv function
    # Read in date columns as string as kwarg date_parser has been depreciated and null dates raise errors
    # with kwarg date_format
    kwargs = {
        'filepath_or_buffer': path,
        'dtype': {k: v if v != 'datetime64[s]' else "object" for k, v in schema.items()},
        'usecols': schema.keys(),
        'cache_dates': True,
        'engine': 'pyarrow',
        # 'parse_dates': [key for key, val in schema.items() if val == 'datetime64[s]'],
        # 'date_format': "%Y-%m-%d",
        # 'date_parser': lambda x: pd.to_datetime(x, format="%Y-%m-%d", errors='coerce')
    }

    # Trigger the used column selection
    if not usecols:
        del kwargs['usecols']

    # Read the csv data into a pandas dataframe object
    data = pd.read_csv(**kwargs)

    # Apply datetime formatting to date columns - coerce nulls to pd.NaT
    for col in [key for key, val in schema.items() if val == "datetime64[s]"]:
        data[col] = pd.to_datetime(data[col], format="%Y-%m-%d", errors='coerce').astype('datetime64[s]')

    # Ensure dataframe datatypes match the schema
    data = enforce_data_types(data)

    # Return the pandas dataframe object
    return data


def read_parquet_to_pandas(path: str, schema: dict, usecols: bool = True) -> pd.DataFrame:
    """
    Loads a parquet into a pandas dataframe object
    :param path: path to parquet
    :param schema: dictionary containing column datatypes
    :param usecols: Boolean to choose only loading columns defined in the schema
    :return: pandas dataframe object containing the parquet data
    """
    logger.info(f"Loading columns: {list(schema.keys())}")

    # Define key word arguments - parquet files store dtypes in metadata so schema is not required when reading
    kwargs = {
        'path': path,
        'columns': schema.keys(),
        'engine': 'pyarrow',
        'dtype_backend': 'numpy_nullable'
    }

    # Trigger the used column selection
    if not usecols:
        del kwargs['columns']

    # Read the parquet data into a pandas dataframe object
    data = pd.read_parquet(**kwargs)

    # Add datatypes from schema in case parquet file was created incorrectly
    for column in data.columns:
        data[column] = data[column].astype(schema[column])

    # Ensure dataframe datatypes match the schema
    data = enforce_data_types(data)

    # Return the pandas dataframe object
    return data


def read_csv_to_spark(path: str, schema: dict) -> pd.DataFrame:
    # TODO: Fill in this method
    pass


def read_parquet_to_spark(path: str, schema: dict) -> pd.DataFrame:
    # TODO: Fill in this method
    pass


def write_csv_from_pandas(data: pd.DataFrame, path: str, schema: dict) -> None:
    """
    Save dataframe data to csv file
    :param data: pandas dataframe object
    :param path: path to save csv file
    :param schema: dictionary containing column datatypes
    """
    # Define the key word arguments
    kwargs = {'path_or_buf': path, 'na_rep': "", 'columns': schema.keys(), 'index': False}

    # Save data to csv file
    data.to_csv(**kwargs)


def write_parquet_from_pandas(data: pd.DataFrame, path: str, schema: dict) -> None:
    """
    Save dataframe data to parquet file
    :param data: pandas dataframe object
    :param path: path to save parquet file
    :param schema: dictionary containing column datatypes
    """
    # Define the key word arguments
    kwargs = {'path': path, 'partition_cols': schema.keys(), 'index': False, 'engine': 'pyarrow', 'compression': 'gzip'}

    # Save data to parquet file
    data.to_parquet(**kwargs)


def write_zip_from_pandas(data: pd.DataFrame, path: str, schema: dict) -> None:
    """
    Save dataframe data to zip file
    :param data: pandas dataframe object
    :param path: path to save zip file
    :param schema: dictionary containing column datatypes
    """
    # Define key word arguments
    kwargs = {'path_or_buf': path, 'na_rep': "", 'columns': schema.keys(), 'index': False,
              'compression': {'method': 'zip'}}

    # Save data to zip file
    data.to_csv(**kwargs)


def write_csv_from_spark(data: pd.DataFrame, path: str, schema: dict, dataframe_name: str = "") -> None:
    # TODO: Fill in this method
    pass


def write_parquet_from_spark(data: pd.DataFrame, path: str, schema: dict) -> None:
    # TODO: Fill in this method
    pass


def write_zip_from_spark(ata: pd.DataFrame, path: str, schema: dict) -> None:
    # TODO: Fill in this method
    pass
