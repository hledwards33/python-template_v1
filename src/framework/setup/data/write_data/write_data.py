from abc import ABC, abstractmethod

import pandas as pd

from framework.setup.data.data_checks.check_output_data import DataCheckFactory, IDataCheck
from framework.setup.data.schemas.format_schema import IFormatSchema, SchemaFormatFactory
from framework.setup.data.schemas.read_schema import IReadSchema, SchemaContext, SchemaFactory
from framework.setup.data.write_data.save_file import SaveFileFactory, ISaveFile, SaveFileContext


class WriteDataContext:
    def __init__(self, data, schema_path: str, data_path: str, model_type: str):
        self.schema_path = schema_path
        self.data_path = data_path
        self.model_type = model_type
        self.data = data


class IDataBuilder(ABC):
    def __init__(self, context: WriteDataContext):
        self.context = context
        self.schema_reader = self.set_schema_reader()
        self.schema_formatter = self.set_schema_formatter()
        self.file_saver = self.set_file_saver()
        self.data_checker = self.set_data_checker()

    @abstractmethod
    def set_schema_reader(self):
        pass

    @abstractmethod
    def set_schema_formatter(self):
        pass

    @abstractmethod
    def set_data_checker(self):
        pass

    @abstractmethod
    def set_file_saver(self):
        pass


class WriteDataBuilder(IDataBuilder):

    def set_schema_reader(self) -> IReadSchema:
        schema_context = SchemaContext(self.context.schema_path)
        return SchemaFactory.create_schema_reader(schema_context)

    def set_schema_formatter(self) -> IFormatSchema:
        self.context.schema = SchemaFormatFactory.get_schema_formatter(self.context.model_type)
        return self.context.schema

    def set_data_checker(self) -> IDataCheck:
        return DataCheckFactory.get_data_checker(self.context.model_type)

    def set_file_saver(self) -> ISaveFile:
        file_context = SaveFileContext(self.context.data_path, self.context.model_type)
        return SaveFileFactory.create_file_saver(file_context)


class WriteDataDirector:
    def __init__(self, builder: DataBuilder):
        self.builder = builder

    @staticmethod
    def remove_columns(data: pd.DataFrame, schema: dict) -> pd.DataFrame:
        return data[schema.keys()]

    def write_data(self):
        schema = self.builder.schema_reader.read_schema()
        formatted_schema = self.builder.schema_formatter.format_schema(schema)
        errors = self.builder.data_checker.check_data(data, formatted_schema)
        self.builder.file_saver.save_file()
        return errors
