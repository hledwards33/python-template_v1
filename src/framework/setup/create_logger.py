import logging
import os
import sys
import threading
from abc import ABC, abstractmethod
from datetime import datetime
from logging import LogRecord
from typing import Callable


class CustomFormatter(logging.Formatter):
    grey = '\x1b[38;21m'
    blue = '\x1b[38;5;39m'
    yellow = '\x1b[38;5;226m'
    red = '\x1b[38;5;196m'
    bold_red = '\x1b[31;1m'
    reset = '\x1b[0m'

    def __init__(self, fmt):
        super().__init__()
        self.fmt = fmt
        self.FORMATS = {
            logging.DEBUG: self.grey + self.fmt + self.reset,
            logging.INFO: self.blue + self.fmt + self.reset,
            logging.WARNING: self.yellow + self.fmt + self.reset,
            logging.ERROR: self.red + self.fmt + self.reset,
            logging.CRITICAL: self.bold_red + self.fmt + self.reset
        }

    def format(self, record) -> logging.Formatter.format:
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


class SingletonMeta(type):
    _instances: dict = {}
    _lock: threading.Lock = threading.Lock()

    def __init__(cls):
        cls._instances[cls] = super().__init__(cls)

    def __new__(cls):
        return cls._instances[cls]


class ILogBuilder(ABC):
    @abstractmethod
    def build_logger(self, **kwargs) -> any:
        pass

    @staticmethod
    def build_handler_filters(handler: str) -> Callable[[LogRecord], bool]:
        def handler_filter(record: logging.LogRecord) -> bool:
            if hasattr(record, 'block'):
                if handler in record.block:
                    return False
            return True

        return handler_filter

    def headers(message: str) -> None:
        line_length = 75
        line_num_start = line_length - math.ceil(len(message) / 2)
        line_num_end = line_num_start if len(message) % 2 == 0 else line_num_start + 1
        lines_start = ''.join(['-' for _ in range(line_num_start)])
        lines_end = ''.join(['-' for _ in range(line_num_end)])
        print()
        print(lines_start + ' ' + message + ' ' + lines_end)
        print()

        simple_file_format()
        logging.info("", extra={'block': ['console']})
        logging.info(lines_start + ' ' + message + ' ' + lines_end + "\n", extra={'block': ['console']})
        detailed_file_format()

    def no_format(message: str) -> None:
        simple_file_format()
        logging.info(message, extra={'block': ['console']})
        print(message)
        detailed_file_format()


class IFileLogBuilder(ILogBuilder):
    def build_logger(self, path: str) -> logging.FileHandler:
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


class FileLogBuilderSimple(IFileLogBuilder):

    def build_logger(self, path: str) -> logging.FileHandler:
        fl_handler = logging.FileHandler(path, 'w+')
        fl_format = logging.Formatter("%(message)s")
        fl_handler.setFormatter(fl_format)
        fl_handler.setLevel(logging.DEBUG)
        fl_handler.addFilter(self.build_handler_filters('file'))
        return fl_handler


class FileLogBuilderDetailed(IFileLogBuilder):

    def build_logger(self, path: str) -> logging.FileHandler:
        fl_handler = logging.FileHandler(path, 'w+')
        fl_format = logging.Formatter("[%(asctime)s] %(levelname)s [%(name)s.%(module)s.%(funcName)s:"
                                      " %(lineno)d] %(message)s")
        fl_handler.setFormatter(fl_format)
        fl_handler.setLevel(logging.DEBUG)
        fl_handler.addFilter(self.build_handler_filters('file'))
        return fl_handler


class SysLogBuilderSimple(ILogBuilder):

    def build_logger(self) -> logging.StreamHandler:
        sys_handler = logging.StreamHandler(sys.stdout)
        cn_format = CustomFormatter("%(message)s")
        sys_handler.setFormatter(cn_format)
        sys_handler.setLevel(logging.DEBUG)
        sys_handler.addFilter(self.build_handler_filters('console'))
        return sys_handler


class SysLogBuilderDetailed(ILogBuilder):

    def build_logger(self) -> logging.StreamHandler:
        sys_handler = logging.StreamHandler(sys.stdout)
        cn_format = CustomFormatter(
            "[%(asctime)s] %(levelname)s [%(name)s.%(module)s.%(funcName)s: %(lineno)d] %(message)s")
        sys_handler.setFormatter(cn_format)
        sys_handler.setLevel(logging.DEBUG)
        sys_handler.addFilter(self.build_handler_filters('console'))
        return sys_handler