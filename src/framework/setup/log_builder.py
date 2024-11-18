import logging
import math
import os
import threading
from datetime import datetime

from log_handlers import IFileHandler, ISysHandler, SysHandlerSimple


class SingletonMeta(type):
    """This is a lazy loading implementation of the Singleton Pattern"""
    _instances: dict = {}
    _lock: threading.Lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                cls._instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
            return cls._instances[cls]


class LogBuilder(metaclass=SingletonMeta):

    def __init__(self, SysHandler: ISysHandler = SysHandlerSimple, FileHandler: IFileHandler = None):
        self._sys_handler = SysHandler
        self._file_handler = FileHandler

    @property
    def file_handler(self):
        return self._file_handler

    @property
    def sys_handler(self):
        return self._sys_handler

    @file_handler.setter
    def file_handler(self, file_handler: IFileHandler):
        self._file_handler = file_handler

    @sys_handler.setter
    def sys_handler(self, sys_handler: ISysHandler):
        self._sys_handler = sys_handler

    def create_logging_file(self, file_handler, path: str, name: str, data_name: str = None) -> None:
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

    def headers(self, message: str) -> None:
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

    def lines(self) -> None:
        output = "".join(["-" for _ in range(152)])

        print(output)

        simple_file_format()
        logging.info(output, extra={'block': ['console']})
        detailed_file_format()

    def no_format(message: str) -> None:
        simple_file_format()
        logging.info(message, extra={'block': ['console']})
        print(message)
        detailed_file_format()
