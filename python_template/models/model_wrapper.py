import pandas as pd


class ModelWrapper:

    def __init__(self):
        pass

    @staticmethod
    def read_config():
        pass

    @staticmethod
    def set_parameters_from_dataframe(data: pd.DataFrame) -> pd.DataFrame:
        pass

    @staticmethod
    def data_pre_processing(data: dict) -> dict:
        pass

    @staticmethod
    def data_post_processing(data: dict) -> dict:
        pass

    @staticmethod
    def read_data(path: str, file_schemas: dict) -> dict:
        pass

    @staticmethod
    def write_data(path: str, file_schemas: dict) -> dict:
        pass
