import logging
import math
import os
import re
from abc import abstractmethod
from datetime import datetime

from framework.setup.logs.log_handlers import SysHandlerSimple, FileHandlerSimple
from framework.setup.meta_classes.singleton import ThreadSafeSingletonABCMeta
from log_handlers import (IFileHandler, ISysHandler, SysHandlerDetailed,
                          FileHandlerDetailed)


class ILogBuilder(metaclass=ThreadSafeSingletonABCMeta):
    __build_status: bool = False  # Initiating a private class variable

    def __init__(self):
        self._sys_handler: ISysHandler = None
        self._file_handler: IFileHandler = None

    @abstractmethod
    def initiate_file_logging(self, *args, **kwargs) -> None:
        pass

    @abstractmethod
    def initiate_sys_logging(self) -> None:
        pass

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

    def expected_file_format(self) -> None:
        for handler in logging.getLogger().handlers:
            if isinstance(handler, logging.FileHandler):
                fl_format = logging.Formatter(self._file_handler.format)
                handler.setFormatter(fl_format)

    @staticmethod
    def simple_file_format() -> None:
        for handler in logging.getLogger().handlers:
            if isinstance(handler, logging.FileHandler):
                handler.setFormatter(logging.Formatter('%(message)s'))

    def headers(self, message: str) -> None:
        line_length = 75
        line_num_start = line_length - math.ceil(len(message) / 2)
        line_num_end = line_num_start if len(message) % 2 == 0 else line_num_start + 1
        lines_start = ''.join(['-' for _ in range(line_num_start)])
        lines_end = ''.join(['-' for _ in range(line_num_end)])
        print()
        print(lines_start + ' ' + message + ' ' + lines_end)
        print()

        self.simple_file_format()
        logging.info("", extra={'block': ['console']})
        logging.info(lines_start + ' ' + message + ' ' + lines_end + "\n", extra={'block': ['console']})
        self.expected_file_format()

    def lines(self) -> None:
        output = "".join(["-" for _ in range(152)])

        print(output)

        self.simple_file_format()
        logging.info(output, extra={'block': ['console']})
        self.expected_file_format()

    def no_format(self, message: str) -> None:
        self.simple_file_format()
        logging.info(message, extra={'block': ['console']})
        print(message)
        self.expected_file_format()

    def update_build_status(self) -> None:
        self.__build_status = not self.__build_status

    @staticmethod
    def terminate_logging(self, name) -> None:
        name = re.sub(r"\{.*?}", "", name)

        for handler in logging.getLogger().handlers:
            if name in str(handler):
                logging.getLogger().removeHandler(handler)

        self.update_build_status()


class ISysAndFileLogBuilder(ILogBuilder):
    def __init__(self):
        super().__init__()
        self._sys_handler = None
        self._file_handler = None

    def initiate_sys_logging(self) -> None:
        logging.getLogger().setLevel(logging.DEBUG)
        logging.getLogger().addHandler(self._sys_handler.handler())

    def initiate_file_logging(self, path: str, name: str, data_name: str = None) -> None:

        format_dict = {}
        if '{date}' in name:
            format_dict['date'] = datetime.date.today()

        if '{data}' in name:
            format_dict['data'] = data_name

        if format_dict:
            name = name.format(**format_dict)

        if sum([1 for handler in logging.getLogger().handlers if name in str(handler)]) < 1:
            file_handler = self._file_handler.handler(os.path.join(path, name) + ".log")
            logging.getLogger().addHandler(file_handler)


class ISysLogBuilder(ILogBuilder):
    def __init__(self):
        super().__init__()
        self._sys_handler = None
        self._file_handler = None

    def initiate_sys_logging(self) -> None:
        logging.getLogger().setLevel(logging.DEBUG)
        logging.getLogger().addHandler(self._sys_handler.handler())

    def initiate_file_logging(self, path: str, name: str, data_name: str = None) -> None:

        format_dict = {}
        if '{date}' in name:
            format_dict['date'] = datetime.date.today()

        if '{data}' in name:
            format_dict['data'] = data_name

        if format_dict:
            name = name.format(**format_dict)

        if sum([1 for handler in logging.getLogger().handlers if name in str(handler)]) < 1:
            file_handler = self._file_handler.handler(os.path.join(path, name) + ".log")
            logging.getLogger().addHandler(file_handler)


class SimpleSysAndFileLogBuilder(ISysAndFileLogBuilder):
    def __init__(self):
        super().__init__()
        self._sys_handler = SysHandlerSimple()
        self._file_handler = FileHandlerSimple()


class DetailedSysAndFileLogBuilder(ISysAndFileLogBuilder):
    def __init__(self):
        super().__init__()
        self._sys_handler = SysHandlerDetailed()
        self._file_handler = FileHandlerDetailed()


class SimpleSysLogBuilder(ISysLogBuilder):
    def __init__(self):
        super().__init__()
        self._sys_handler = SysHandlerSimple()
        self._file_handler = None


class DetailedSysLogBuilder(ISysLogBuilder):
    def __init__(self):
        super().__init__()
        self._sys_handler = SysHandlerDetailed()
        self._file_handler = None


class SimpleFileLogBuilder(ISysLogBuilder):
    def __init__(self):
        super().__init__()
        self._sys_handler = None
        self._file_handler = FileHandlerSimple()


class DetailedFileLogBuilder(ISysLogBuilder):
    def __init__(self):
        super().__init__()
        self._sys_handler = None
        self._file_handler = FileHandlerDetailed()


class LoggingDirector:
    def __init__(self, builder: ILogBuilder):
        self.builder = builder

    def initiate_logging(self, *args, **kwargs) -> None:
        if not self.builder.__build_status:
            self.builder.initiate_file_logging(*args, **kwargs)
            self.builder.initiate_sys_logging()
            self.builder.update_build_status()
        else:
            logging.info("Logging has already been initiated.")
