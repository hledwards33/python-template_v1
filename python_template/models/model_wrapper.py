import pandas as pd


class ModelWrapper:

    def __int__(self):
        pass

    @staticmethod
    def data_pre_processing(data: dict) -> dict:
        pass

    @staticmethod
    def set_parameters_from_dataframe(data: pd.DataFrame) -> pd.DataFrame:
        pass

    @staticmethod
    def data_post_processing(data: dict) -> dict:
        pass
