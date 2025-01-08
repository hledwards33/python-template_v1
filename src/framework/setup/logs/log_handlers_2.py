import logging
import sys
from abc import ABC, abstractmethod
from logging import LogRecord
from typing import Callable

from framework.setup.logs.log_formaters import ColourfulSysFormatter


class LogHandlerContext:
    def __init__(self, log_file_path: str):
        self.log_file_path = log_file_path
        self.file_logging = True if log_file_path != "" else False


class ILogHandler(ABC):

    def __init__(self):
        self.format: str = ""
        self.formatter = None

    @abstractmethod
    def handler(self, **kwargs) -> logging.FileHandler:
        pass

    @staticmethod
    def build_handler_filters(handler: str) -> Callable[[LogRecord], bool]:
        def handler_filter(record: logging.LogRecord) -> bool:
            if hasattr(record, 'block'):
                if handler in record.block:
                    return False
            return True

        return handler_filter


class IFileHandler(ILogHandler):

    def __init__(self, formatter: logging.Formatter = logging.Formatter):
        super().__init__()

    def handler(self, path: str) -> logging.FileHandler:
        pass


class FileHandlerSimple(IFileHandler):

    def __init__(self):
        super().__init__()
        self.format = "%(message)s"
        self.formatter = logging.Formatter(self.format)

    def handler(self, path: str) -> logging.FileHandler:
        fl_handler = logging.FileHandler(path, 'w+')
        fl_handler.setFormatter(self.formatter)
        fl_handler.setLevel(logging.DEBUG)
        fl_handler.addFilter(self.build_handler_filters('file'))
        return fl_handler


class FileHandlerDetailed(IFileHandler):

    def __init__(self):
        super().__init__()
        self.format = "[%(asctime)s] %(levelname)s [%(name)s.%(module)s.%(funcName)s: %(lineno)d] %(message)s"
        self.formatter = logging.Formatter(self.format)

    def handler(self, path: str) -> logging.FileHandler:
        fl_handler = logging.FileHandler(path, 'w+')
        fl_handler.setFormatter(self.formatter)
        fl_handler.setLevel(logging.DEBUG)
        fl_handler.addFilter(self.build_handler_filters('file'))
        return fl_handler


class ISysHandler(ILogHandler):

    def __init__(self):
        super().__init__()

    def handler(self) -> logging.StreamHandler:
        pass


class SysHandlerSimple(ISysHandler):

    def __init__(self):
        super().__init__()
        self.format = "%(message)s"
        self.formatter = ColourfulSysFormatter(self.format)

    def handler(self) -> logging.StreamHandler:
        sys_handler = logging.StreamHandler(sys.stdout)
        sys_handler.setFormatter(self.formatter)
        sys_handler.setLevel(logging.DEBUG)
        sys_handler.addFilter(self.build_handler_filters('console'))
        return sys_handler


class SysHandlerDetailed(ISysHandler):

    def __init__(self):
        super().__init__()
        self.format = "[%(asctime)s] %(levelname)s [%(name)s.%(module)s.%(funcName)s: %(lineno)d] %(message)s"
        self.formatter = ColourfulSysFormatter(self.format)

    def handler(self) -> logging.StreamHandler:
        sys_handler = logging.StreamHandler(sys.stdout)
        sys_handler.setFormatter(self.formatter)
        sys_handler.setLevel(logging.DEBUG)
        sys_handler.addFilter(self.build_handler_filters('console'))
        return sys_handler


class LogHandlerFactory:

    def __init__(self, context: LogHandlerContext):
        self.context = context

    @staticmethod
    def create_sys_handler(log_type: str) -> ILogHandler:
        match log_type:
            case 'simple':
                return SysHandlerSimple()
            case 'detailed':
                return SysHandlerDetailed()
            case _:
                raise ValueError(f"Invalid log type: {log_type}.")

    @staticmethod
    def create_file_handler(log_type: str) -> ILogHandler:
        match log_type:
            case 'simple':
                return FileHandlerSimple()
            case 'detailed':
                return FileHandlerDetailed()
            case _:
                raise ValueError(f"Invalid log type: {log_type}.")
