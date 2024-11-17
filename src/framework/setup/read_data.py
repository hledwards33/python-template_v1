from abc import ABC, abstractmethod


class IReadFile(ABC):
    @abstractmethod
    def read(self, path):
        pass


class ReadCSV2Pandas(IReadFile):
    def read(self, path):
        pass


class ReadParquet2Pandas(IReadFile):
    def read(self, path):
        pass


class ReadCSV2Spark(IReadFile):
    def read(self, path):
        pass


class ReadJson2Dict(IReadFile):
    def read(self, path):
        pass


class ReadYaml2Dict(IReadFile):
    def read(self, path):
        pass
