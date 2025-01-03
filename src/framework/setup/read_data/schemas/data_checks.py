from abc import ABC, abstractmethod

from framework.setup.read_data.schemas.type_complexities import ModelType

class IDataCheck(ABC):
    @abstractmethod
    def check_data(self, data):
        pass

class PandasDataCheck(IDataCheck):
    def check_data(self, data):
        pass

class SparkDataCheck(IDataCheck):
    def check_data(self, data):
        # TODO: Implement this method
        pass

class DataCheckFactory:
    @staticmethod
    def get_data_checker(model_type: ModelType) -> IDataCheck:
        if model_type == ModelType.PANDAS:
            return PandasDataCheck()
        elif model_type == ModelType.SPARK:
            return SparkDataCheck()
        else:
            raise ValueError("Invalid model type")