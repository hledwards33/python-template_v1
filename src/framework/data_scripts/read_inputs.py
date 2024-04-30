import json

import pandas as pd
import yaml


class InputData:

    def __init__(self):
        pass

    @staticmethod
    def read_csv(path: str, schema: dict) -> pd.DataFrame:
        # TODO: Log dataset x is being read in, only columns defined in schemas are read
        # TODO: Check if this works with zip files and add if_zip to the read data func
        kwargs = {'path': path, 'dtype': schema, 'usecols': schema.keys(), 'cache_dates': True,
                  'infer_datetime_format': False, 'engine': 'pyarrow',
                  'parse_dates': [key for key, val in schema.items() if val == "date"],
                  'date_format': "%Y-%m-%d"}

        data = pd.read_csv(**kwargs)

        return data

    @staticmethod
    def read_parquet(path: str, schema: dict) -> pd.DataFrame:
        # TODO: Fill in this method
        pass

    @staticmethod
    def read_json(path: str) -> dict:
        with open(path, 'r') as file:
            result = json.load(file)

        return result

    @staticmethod
    def read_yaml(path: str) -> dict:
        with open(path, 'r') as file:
            result = yaml.load(file)

        return result
