from abc import ABC, abstractmethod

from framework.setup.read_data.schemas.format_schema import IFormatSchema, SchemaFormatFactory
from framework.setup.read_data.schemas.load_file import FileContext, LoadFileFactory
from framework.setup.read_data.schemas.read_schema import IReadSchema, SchemaContext, SchemaFactory


class DataContext:
    def __init__(self, schema_path: str, data_path: str, model_type: str):
        self.schema_path = schema_path
        self.data_path = data_path
        self.model_type = model_type
        self._schema = None

    @property
    def schema(self):
        return self._schema

    @schema.setter
    def schema(self, schema):
        self._schema = schema


class IDataBuilder(ABC):
    def __init__(self, context: DataContext):
        self.context = context
        self.schema_reader = self.set_schema_reader()
        self.schema_formatter = self.set_schema_formatter()
        self.file_loader = self.set_file_loader()

    @abstractmethod
    def set_schema_reader(self):
        pass

    @abstractmethod
    def set_schema_formatter(self):
        pass

    @abstractmethod
    def set_file_loader(self):
        pass


class DataBuilder(IDataBuilder):

    def set_schema_reader(self) -> IReadSchema:
        schema_context = SchemaContext(self.context.schema_path)
        return SchemaFactory.create_schema_reader(schema_context)

    def set_schema_formatter(self) -> IFormatSchema:
        self.context.schema = SchemaFormatFactory.get_schema_formatter(self.context.model_type)
        return self.context.schema

    def set_file_loader(self):
        file_context = FileContext(self.context.data_path)
        return LoadFileFactory.create_file_loader(file_context)


class DataDirector:
    def __init__(self, builder: DataBuilder):
        self.builder = builder

    def read_data(self):
        schema = self.builder.schema_reader.read_schema()
        formatted_schema = self.builder.schema_formatter.format_schema(schema)
        data = self.builder.file_loader.load_file(formatted_schema)
        # TODO: Add the other steps here
        return data
