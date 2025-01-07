import logging
import os
from abc import ABC, abstractmethod

import pandas as pd

from framework.setup.data.type_complexities import FileExtension

logger = logging.getLogger()


class ISaveFile(ABC):
    def __init__(self, data_path: str):
        self.data_path = data_path

    @abstractmethod
    def save_file(self, schema: dict):
        pass


class ISavePandas2File(ISaveFile):
    @abstractmethod
    def save_file(self, schema: dict) -> pd.DataFrame:
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


class SavePandas2CSV(ISavePandas2File):
    def save_file(self, data: pd.DataFrame):
        pass


class SaveParquet2Pandas(ISavePandas2File):
    def save_file(self, schema: dict) -> pd.DataFrame:
        pass


class FileContext:
    def __init__(self, data_path: str):
        self.data_path = data_path
        self.data_extension = data_path.split(".")[-1].lower()


class LoadFileFactory:
    @staticmethod
    def create_file_loader(context: FileContext) -> ISaveFile:
        match context.data_extension:
            case FileExtension.CSV.value | FileExtension.ZIP.value:
                return SavePandas2CSV(context.data_path)
            case FileExtension.PARQUET.value | FileExtension.PQT.value:
                return SaveParquet2Pandas(context.data_path)
            case _:
                raise ValueError(f"Unsupported file type: {context.data_extension}.")
