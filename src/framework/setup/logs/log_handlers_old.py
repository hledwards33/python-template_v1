import logging
import sys
from abc import ABC, abstractmethod
from logging import LogRecord
from typing import Callable

from framework.setup.logs.log_formaters import ColourfulSysFormatter


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
