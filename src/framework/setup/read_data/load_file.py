import logging
import os
from abc import ABC, abstractmethod

import pandas as pd

from framework.setup.read_data.type_complexities import FileExtension

logger = logging.getLogger()


class ILoadFile(ABC):
    def __init__(self, data_path: str):
        self.data_path = data_path

    @abstractmethod
    def load_file(self, schema: dict):
        pass


class ILoadFile2Pandas(ILoadFile):
    @abstractmethod
    def load_file(self, schema: dict) -> pd.DataFrame:
        pass

    @staticmethod
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

    @staticmethod
    def enforce_floats(df: pd.DataFrame) -> pd.DataFrame:
        """
        Standardises the float fields in any given dataframe
        :param df: pandas dataframe object
        :return: pandas dataframe with standardised float fields
        """
        # Loop through each column and standardise float fields
        for column in df.columns:
            if df[column].dtype == "Float64":
                df[column] = df[column].astype("Float64")

        # Return a dataframe with standardised float fields
        return df

    @staticmethod
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

    def enforce_dates(self, df: pd.DataFrame, schema: dict) -> pd.DataFrame:
        # Apply datetime formatting to date columns - coerce nulls to pd.NaT
        for col in [key for key, val in schema.items() if val == "datetime64[s]"]:
            df[col] = pd.to_datetime(df[col], format="%Y-%m-%d", errors='coerce').astype('datetime64[s]')

            # Check for date columns that have been unsuccessfully converted to datetime
            if df[col].isna().all():
                logger.warning(f"Date column {col} in dataset {os.path.split(self.data_path)[-1]} contains all null "
                               f"data values. Check that the raw data contains dates in ISO format (yyyy-mm-dd).")

        # Return a dataframe with standardised date fields
        return df

    def enforce_data_types(self, df: pd.DataFrame, schema: dict) -> pd.DataFrame:

        # Standardise date values
        df = self.enforce_dates(df, schema)

        # Standardise integer values
        df = self.enforce_integers(df)

        # Standardise float values
        df = self.enforce_floats(df)

        # Standardise string values
        df = self.enforce_strings(df)

        # Return a dataframe with standardised values
        return df


class ReadCSV2Pandas(ILoadFile2Pandas):
    def load_file(self, schema: dict) -> pd.DataFrame:
        """
        Loads a csv or zipped csv into a pandas dataframe object
        :return: pandas dataframe object containing the csv data
        """
        logger.info(f"Loading columns: {list(schema.keys())}")

        # Define the key word arguments to be supplied to the pandas.read_csv function
        # Read in date columns as string as kwarg date_parser has been depreciated and null dates raise errors
        # with kwarg date_format
        parameters = {
            'filepath_or_buffer': self.data_path,
            'dtype': {k: v if v != 'datetime64[s]' else "object" for k, v in schema.items()},
            'usecols': schema.keys(),
            'cache_dates': True,
            'engine': 'pyarrow',
        }

        # Read the csv data into a pandas dataframe object
        data = pd.read_csv(**parameters)

        # Ensure dataframe datatypes match the schema
        data = self.enforce_data_types(data, schema)

        # Return the pandas dataframe object
        return data


class ReadParquet2Pandas(ILoadFile2Pandas):
    def load_file(self, schema: dict) -> pd.DataFrame:
        logger.info(f"Loading columns: {list(schema.keys())}")

        # Define key word arguments - parquet files store dtypes in metadata so schema is not required when reading
        kwargs = {
            'path': self.data_path,
            'columns': schema.keys(),
            'engine': 'pyarrow',
            'dtype_backend': 'numpy_nullable'
        }

        # Read the parquet data into a pandas dataframe object
        data = pd.read_parquet(**kwargs)

        # Add datatypes from the schema incase the parquet file was created incorrectly
        for column in data.columns:
            data[column] = data[column].astype(schema[column])

        # Ensure dataframe datatypes match the schema
        data = self.enforce_data_types(data, schema)

        # Return the pandas dataframe object
        return data


class FileContext:
    def __init__(self, data_path: str):
        self.data_path = data_path
        self.data_extension = data_path.split(".")[-1].lower()


class LoadFileFactory:
    @staticmethod
    def create_file_loader(context: FileContext) -> ILoadFile:
        match context.data_extension:
            case FileExtension.CSV.value | FileExtension.ZIP.value:
                return ReadCSV2Pandas(context.data_path)
            case FileExtension.PARQUET.value | FileExtension.PQT.value:
                return ReadParquet2Pandas(context.data_path)
            case _:
                raise ValueError(f"Unsupported file type: {context.data_extension}.")
