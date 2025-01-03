from abc import ABC, abstractmethod

from framework.setup.read_data.schemas.format_schema import IFormatSchema, SchemaFormatFactory
from framework.setup.read_data.schemas.read_schema import IReadSchema, SchemaContext, SchemaFactory


class DataContext:
    def __init__(self, schema_path: str, data_path: str, model_type: str):
        self.schema_path = schema_path
        self.data_path = data_path
        self.model_type = model_type


class IDataBuilder(ABC):
    def __init__(self, context: DataContext):
        self.context = context
        self.schema_reader = self.set_schema_reader()
        self.schema_formatter = self.set_schema_formatter()

    @abstractmethod
    def set_schema_reader(self):
        pass

    @abstractmethod
    def set_schema_formatter(self):
        pass


class DataBuilder(IDataBuilder):

    def set_schema_reader(self) -> IReadSchema:
        schema_context = SchemaContext(self.context.schema_path)
        return SchemaFactory.create_schema_reader(schema_context)

    def set_schema_formatter(self) -> IFormatSchema:
        return SchemaFormatFactory.get_schema_formatter(self.context.model_type)


class DataDirector:
    def __init__(self, builder: DataBuilder):
        self.builder = builder

    def read_data(self):
        schema = self.builder.schema_reader.read_schema()
        formatted_schema = self.builder.schema_formatter.format_schema(schema)
        # TODO: Add the other steps here
        return formatted_schema
