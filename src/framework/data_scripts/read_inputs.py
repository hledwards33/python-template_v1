import json

import pandas as pd
import yaml


class InputData:

    def __init__(self):
        pass

    @staticmethod
    def read_json(path: str) -> dict:
        with open(path, 'r') as file:
            result = json.load(file)

        return result

    @staticmethod
    def read_yaml(path: str) -> dict:
        with open(path, 'r') as file:
            result = yaml.safe_load(file)

        return result

    @staticmethod
    def convert_schema_pandas(schema: dict) -> dict:

        for key, val in schema.items():
            if val.lower() == 'integer':
                schema[key] = pd.Int64Dtype
            elif val.lower() == 'float':
                schema[key] = pd.Float64Dtype
            elif val.lower() == 'date':
                schema[key] = 'datetime64[D]'
            elif val.lower() == 'string':
                schema[key] = 'object'

        return schema

    @staticmethod
    def convert_schema_spark(schema: dict) -> dict:
        pass

    @staticmethod
    def schema_conformance_spark():
        pass

    def schema_conformance_pandas(self, data: pd.DataFrame, schema: dict, dataframe_name: str = ""):
        # TODO: improve this function so all errors are raised at once

        extra_cols = set(data.columns).difference(schema.keys())
        # Log: extra columns... have been dropped

        missing_cols = set(schema.keys()).difference(data.columns)
        if len(missing_cols) > 0:
            raise KeyError(f"Dataframe {dataframe_name} is missing the following columns {missing_cols}.")

        schema = self.convert_schema_pandas(schema)
        for col in data.columns:
            if data[col].dtype == schema[col]:
                # TODO: log that datat is correct
                pass
            else:
                raise TypeError(f"Dataframe {dataframe_name} has incorrect datatype in {col} expected {schema[col]} "
                                f"got {data[col].dtype}.")

    def read_csv_to_pandas(self, path: str, schema: dict) -> pd.DataFrame:
        # TODO: Log dataset x is being read in, only columns defined in schemas are read
        # TODO: Check if this works with zip files and add if_zip to the read data func
        kwargs = {
            'path': path,
            'dtype': self.convert_schema_pandas(schema),
            'usecols': schema.keys(),
            'cache_dates': True,
            'infer_datetime_format': False,
            'engine': 'pyarrow',
            'parse_dates': [key for key, val in schema.items() if val == "date"],
            'date_format': "%Y-%m-%d"
        }

        data = pd.read_csv(**kwargs)

        return data

    @staticmethod
    def read_parquet_to_pandas(path: str, schema: dict) -> pd.DataFrame:
        # TODO: Fill in this method
        pass

    @staticmethod
    def read_csv_to_spark(path: str, schema: dict) -> pd.DataFrame:
        # TODO: Fill in this method
        pass

    @staticmethod
    def read_parquet_to_spark(path: str, schema: dict) -> pd.DataFrame:
        # TODO: Fill in this method
        pass

    @staticmethod
    def write_csv_from_pandas(data: pd.DataFrame, path: str, schema: dict, dataframe_name: str = ""):

        extra_cols = set(data.columns).difference(schema.keys())
        # Log: extra columns... have been dropped

        missing_cols = set(schema.keys()).difference(data.columns)
        if len(missing_cols) > 0:
            raise KeyError(f"Dataframe {dataframe_name} is missing the following columns {missing_cols}.")

    @staticmethod
    def write_parquet_from_pandas(data: pd.DataFrame, path: str, schema: dict):
        # TODO: Fill in this method
        pass
