import logging
from abc import ABC, abstractmethod

import pandas as pd

from framework.setup.data.type_complexities import FileExtension

logger = logging.getLogger()


class ISaveFile(ABC):
    def __init__(self, data_path: str):
        self.data_path = data_path

    @abstractmethod
    def save_file(self, data: pd.DataFrame):
        pass


class ISavePandas2File(ISaveFile):
    def save_file(self, data: pd.DataFrame):
        pass


class ISaveSpark2File(ISaveFile):
    def save_file(self, data):
        pass


class SavePandas2CSV(ISavePandas2File):
    def save_file(self, data: pd.DataFrame):
        pass


class SaveParquet2Pandas(ISavePandas2File):
    def save_file(self, schema: dict) -> pd.DataFrame:
        pass


class SaveFileContext:
    def __init__(self, data_path: str, model_type: str):
        self.data_path = data_path
        self.data_extension = data_path.split(".")[-1].lower()
        self.model_type = model_type


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
