import logging
import math
import os
import re
from abc import abstractmethod
from datetime import datetime

from framework.setup.logs.log_handlers import LogHandlerFactory
from framework.setup.structures.meta_classes.singleton import ThreadSafeSingletonABCMeta

logger = logging.getLogger()


class LogHandler:
    def __init__(self, log_file_path: str):
        self.sys_handler = None
        self.file_handler = None
        self.log_file_path = log_file_path
        self.file_logging = True if log_file_path != "" else False

    @property
    def sys_handler(self):
        return self.sys_handler

    @sys_handler.setter
    def sys_handler(self, value):
        self.sys_handler = value

    @property
    def file_handler(self):
        return self.file_handler

    @file_handler.setter
    def file_handler(self, value):
        self.file_handler = value


class ILogBuilder(metaclass=ThreadSafeSingletonABCMeta):
    __build_status: bool = False  # Initiating a private class variable

    def __init__(self, handler: LogHandler):
        self._handler = handler

    def update_build_status(self):
        self.__build_status = not self.__build_status

    def get_build_status(self) -> bool:
        return self.__build_status

    def initiate_logging(self):
        self.initiate_sys_logging()
        if self._handler.file_logging: self.initiate_file_logging()
        self.update_build_status()

    @abstractmethod
    def initiate_sys_logging(self):
        pass

    @abstractmethod
    def initiate_file_logging(self):
        pass

    def expected_file_format(self) -> None:
        for handler in logging.getLogger().handlers:
            if isinstance(handler, logging.FileHandler):
                fl_format = logging.Formatter(self._handler.file_handler.format)
                handler.setFormatter(fl_format)

    @staticmethod
    def simple_file_format() -> None:
        for handler in logging.getLogger().handlers:
            if isinstance(handler, logging.FileHandler):
                handler.setFormatter(logging.Formatter('%(message)s'))

    # TODO: Consider how the user can call this function - add extra function to utils?
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

    def terminate_logging(self, name) -> None:
        name = re.sub(r"\{.*?}", "", name)

        for handler in logging.getLogger().handlers:
            if name in str(handler):
                logging.getLogger().removeHandler(handler)

        self.update_build_status()


class LogBuilder(ILogBuilder):

    def initiate_logging(self):
        self.initiate_sys_logging()
        self.initiate_file_logging()

    def initiate_sys_logging(self) -> None:
        logging.getLogger().setLevel(logging.DEBUG)
        logging.getLogger().addHandler(self._handler.sys_handler.handler())

    def initiate_file_logging(self):
        name = os.path.split(self._handler.log_file_path)[-1]
        if '{date}' in name: name.format(date=datetime.date.today())

        if sum([1 for handler in logging.getLogger().handlers if name in str(handler)]) < 1:
            file_handler = self._handler.file_handler.handler(self._handler.log_file_path)
            logging.getLogger().addHandler(file_handler)


class LogContext:
    def __init__(self, log_file_path: str, log_type: str):
        self.log_file_path = os.path.normpath(log_file_path)
        self.log_type = log_type


class LogFactory:
    def __init__(self, context: LogContext):
        self.context = context

    @staticmethod
    def create_log_builder(context: LogContext) -> ILogBuilder:
        handler = LogHandler(context.log_file_path)
        match context.log_type:
            case 'simple':
                handler.sys_handler = SysHandlerSimple()
                handler.file_handler = FileHandlerSimple()
            case 'detailed':
                handler.sys_handler = SysHandlerDetailed()
                handler.file_handler = FileHandlerDetailed()
            case _:
                raise ValueError("Invalid log type. Please select from 'simple' or 'detailed'.")

        return LogBuilder(handler)
