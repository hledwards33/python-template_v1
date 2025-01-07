import logging
from abc import ABC, abstractmethod

import pandas as pd

from framework.setup.data.type_complexities import FileExtension, ModelType

logger = logging.getLogger()


class ISaveFile(ABC):
    def __init__(self, data, data_path: str):
        self.data = data
        self.data_path = data_path

    def select_columns(self, schema: dict) -> pd.DataFrame:
        return self.data[schema["columns"]]

    @abstractmethod
    def save_file(self, schema: dict):
        pass


class ISavePandas2File(ISaveFile):
    def save_file(self, schema: dict):
        pass


class ISaveSpark2File(ISaveFile):
    def save_file(self, schema: dict):
        pass


class SavePandas2CSV(ISavePandas2File):
    def save_file(self, schema: dict):
        data = self.select_columns(schema)
        data.to_csv(self.data_path, index=False)


class SaveParquet2Pandas(ISavePandas2File):
    def save_file(self, schema):
        data = self.select_columns(schema)
        data.to_parquet(self.data_path, index=False)


class SaveFileContext:
    def __init__(self, data, data_path: str, model_type: str):
        self.data = data
        self.data_path = data_path
        self.data_extension = data_path.split(".")[-1].lower()
        self.model_type = model_type


class ISaveFileFactoryModelType(ABC):
    @abstractmethod
    def create_file_saver(self, context: SaveFileContext) -> ISaveFile:
        pass


class SaveFileFactoryPandas(ISaveFileFactoryModelType):
    def create_file_saver(self, context: SaveFileContext) -> ISaveFile:
        match context.data_extension:
            case FileExtension.CSV.value | FileExtension.ZIP.value:
                return SavePandas2CSV(context.data, context.data_path)
            case FileExtension.PARQUET.value | FileExtension.PQT.value:
                return SaveParquet2Pandas(context.data, context.data_path)
            case _:
                raise ValueError(f"Unsupported output file type: {context.data_extension}.")


class SaveFileFactorySpark(ISaveFileFactoryModelType):
    def create_file_saver(self, context: SaveFileContext) -> ISaveFile:
        match context.data_extension:
            case FileExtension.CSV.value | FileExtension.ZIP.value:
                # TODO: Implement the Spark Model savers
                raise NotImplementedError("Spark CSV saving not yet implemented.")
            case FileExtension.PARQUET.value | FileExtension.PQT.value:
                # TODO: Implement the Spark Model savers
                raise NotImplementedError("Spark Parquet saving not yet implemented.")
            case _:
                raise ValueError(f"Unsupported output file type: {context.data_extension}.")


class SaveFileFactory:
    @staticmethod
    def create_file_saver(context: SaveFileContext) -> ISaveFile:
        match context.model_type:
            case ModelType.PANDAS.value:
                return SaveFileFactoryPandas().create_file_saver(context)
            case ModelType.SPARK.value:
                return SaveFileFactorySpark().create_file_saver(context)
            case _:
                raise ValueError(f"Unsupported model type: {context.model_type}.")
