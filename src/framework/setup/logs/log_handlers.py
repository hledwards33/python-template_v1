import logging
import os
import sys
from abc import ABC, abstractmethod
from datetime import datetime
from logging import LogRecord
from typing import Callable

from framework.setup.logs.log_formaters import ColourfulSysFormatter


class ILogHandler(ABC):

    def __init__(self, formatter: logging.Formatter = logging.Formatter):
        self.format: str = ""
        self.formatter: logging.Formatter = formatter

    @abstractmethod
    def handler(self, **kwargs) -> any:
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
        super().__init__(formatter)

    def handler(self, path: str) -> logging.FileHandler:
        pass

    @staticmethod
    def create_logging_file(file_handler, path: str, name: str, data_name: str = None) -> None:
        format_dict = {}
        if '{date}' in name:
            format_dict['date'] = datetime.date.today()

        if '{data}' in name:
            format_dict['data'] = data_name

        if format_dict:
            name = name.format(**format_dict)

        if sum([1 for handler in logging.getLogger().handlers if name in str(handler)]) < 1:
            fil_handler = file_handler(os.path.join(path, name) + ".log")
            logging.getLogger().addHandler(fil_handler)


class FileHandlerSimple(IFileHandler):

    def __init__(self, formatter: logging.Formatter = logging.Formatter):
        super().__init__(formatter)
        self.format = "%(message)s"

    def handler(self, path: str) -> logging.FileHandler:
        fl_handler = logging.FileHandler(path, 'w+')
        fl_format = self.formatter(self.format)
        fl_handler.setFormatter(fl_format)
        fl_handler.setLevel(logging.DEBUG)
        fl_handler.addFilter(self.build_handler_filters('file'))
        return fl_handler


class FileHandlerDetailed(IFileHandler):

    def __init__(self, formatter: logging.Formatter = logging.Formatter):
        super().__init__(formatter)
        self.format = "[%(asctime)s] %(levelname)s [%(name)s.%(module)s.%(funcName)s: %(lineno)d] %(message)s"

    def handler(self, path: str) -> logging.FileHandler:
        fl_handler = logging.FileHandler(path, 'w+')
        fl_format = logging.Formatter(self.format)
        fl_handler.setFormatter(fl_format)
        fl_handler.setLevel(logging.DEBUG)
        fl_handler.addFilter(self.build_handler_filters('file'))
        return fl_handler


class ISysHandler(ILogHandler):

    def __init__(self, formatter: logging.Formatter = ColourfulSysFormatter):
        super().__init__(formatter)

    def handler(self) -> logging.StreamHandler:
        pass


class SysHandlerSimple(ISysHandler):

    def __init__(self, formatter: logging.Formatter = ColourfulSysFormatter):
        super().__init__(formatter)
        self.format = "%(message)s"

    def handler(self) -> logging.StreamHandler:
        sys_handler = logging.StreamHandler(sys.stdout)
        cn_format = self.formatter(self.format)
        sys_handler.setFormatter(cn_format)
        sys_handler.setLevel(logging.DEBUG)
        sys_handler.addFilter(self.build_handler_filters('console'))
        return sys_handler


class SysHandlerDetailed(ISysHandler):

    def __init__(self, formatter: logging.Formatter = ColourfulSysFormatter):
        super().__init__(formatter)
        self.format = "[%(asctime)s] %(levelname)s [%(name)s.%(module)s.%(funcName)s: %(lineno)d] %(message)s"

    def handler(self) -> logging.StreamHandler:
        sys_handler = logging.StreamHandler(sys.stdout)
        cn_format = self.formatter(self.format)
        sys_handler.setFormatter(cn_format)
        sys_handler.setLevel(logging.DEBUG)
        sys_handler.addFilter(self.build_handler_filters('console'))
        return sys_handler
