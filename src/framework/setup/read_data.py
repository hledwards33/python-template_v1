import json
import logging
import os
from abc import ABC, abstractmethod

import pandas as pd
import yaml

logger = logging.getLogger()


class IReadFile(ABC):
    @abstractmethod
    def read(self, path: str):
        pass


class IReadFile2Pandas(IReadFile):
    @abstractmethod
    def read(self, path: str, schema: dict = None) -> pd.DataFrame:
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

    def enforce_data_types(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Standardises the values in each column of the passed dataset
        :param df: pandas dataset object
        :return: pandas dataset with standardised values
        """
        # Standardise integer values
        df = self.enforce_integers(df)

        # Standardise float values
        df = self.enforce_floats(df)

        # Standardise string values
        df = self.enforce_strings(df)

        # Return a dataframe with standardised values
        return df


class ReadCSV2Pandas(IReadFile2Pandas):
    def read(self, path: str, schema: dict = None) -> pd.DataFrame:
        """
        Loads a csv or zipped csv into a pandas dataframe object
        :param path: path to csv
        :param schema: dictionary containing the column datatypes
        :return: pandas dataframe object containing the csv data
        """
        logger.info(f"Loading columns: {list(schema.keys())}")

        # Define the key word arguments to be supplied to the pandas.read_csv function
        # Read in date columns as string as kwarg date_parser has been depreciated and null dates raise errors
        # with kwarg date_format
        parameters = {
            'filepath_or_buffer': path,
            'dtype': {k: v if v != 'datetime64[s]' else "object" for k, v in schema.items()},
            'usecols': schema.keys(),
            'cache_dates': True,
            'engine': 'pyarrow',
            # 'parse_dates': [key for key, val in schema.items() if val == 'datetime64[s]'],
            # 'date_format': "%Y-%m-%d",
            # 'date_parser': lambda x: pd.to_datetime(x, format="%Y-%m-%d", errors='coerce')
        }

        # Read the csv data into a pandas dataframe object
        data = pd.read_csv(**parameters)

        # Apply datetime formatting to date columns - coerce nulls to pd.NaT
        for col in [key for key, val in schema.items() if val == "datetime64[s]"]:
            data[col] = pd.to_datetime(data[col], format="%Y-%m-%d", errors='coerce').astype('datetime64[s]')

        # Ensure dataframe datatypes match the schema
        data = self.enforce_data_types(data)

        # Return the pandas dataframe object
        return data


class ReadParquet2Pandas(IReadFile):
    def read(self, path: str, schema: dict = None) -> pd.DataFrame:
        pass


class ReadJson2Dict(IReadFile):
    def read(self, path: str, **kwargs) -> dict:
        """
        Loads a json file into a dictionary object
        :param path: tuple containing imported module and file name
        :return: dictionary containing json file's content
        """

        # Create a string path from the passed arguments
        path = os.path.join(os.path.dirname(path[0].__file__), path[1])

        # Open the json file and load to a dictionary
        with open(path, 'r') as file:
            result: dict = json.load(file)

        # Return json file content within a dictionary object
        return result


class ReadYaml2Dict(IReadFile):
    def read(self, path: str) -> dict:
        """
        Loads a yaml file into a dictionary object
        :param path: string pointing to a yaml file
        :return: dictionary containing yaml file's content
        """
        # Open the yaml file and load to a dictionary
        with open(path, 'r') as file:
            result: dict = yaml.safe_load(file)

        # Return yaml file content within a dictionary object
        return result
