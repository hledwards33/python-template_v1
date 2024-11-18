from abc import ABC, abstractmethod

import pandas as pd


class IWriteData(ABC):
    @abstractmethod
    def write(self, path: str, data: any):
        pass

class IWriteDataFromPandas(IWriteData):
    @abstractmethod
    def write(self, path: str, data: pd.DataFrame, schema: dict = None):
        pass

    @abstractmethod
    def schema_conformance(self, data: pd.DataFrame, schema: dict) -> any:
        pass