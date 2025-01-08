import logging
import math
import os
import re
from abc import abstractmethod
from datetime import datetime

from framework.setup.logs.log_handlers import (SysHandlerDetailed,
                                               FileHandlerDetailed)
from framework.setup.logs.log_handlers import SysHandlerSimple, FileHandlerSimple
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

    @abstractmethod
    def initiate_logging(self, *args, **kwargs):
        pass

    @abstractmethod
    def initiate_sys_logging(self):
        pass

    @abstractmethod
    def initiate_file_logging(self, path: str, name: str):
        pass

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

    def initiate_logging(self, path: str, name: str):
        self.initiate_sys_logging()
        self.initiate_file_logging(path, name)

    def initiate_sys_logging(self) -> None:
        logging.getLogger().setLevel(logging.DEBUG)
        logging.getLogger().addHandler(self._sys_handler.handler())

    def initiate_file_logging(self, path: str, name: str):
        if '{date}' in name: name.format(date=datetime.date.today())

        if sum([1 for handler in logging.getLogger().handlers if name in str(handler)]) < 1:
            file_handler = self._file_handler.handler(os.path.join(path, name) + ".log")
            logging.getLogger().addHandler(file_handler)


class LogContext:
    def __init__(self, log_file_path: str, log_type: str):
        self.log_file_path = log_file_path
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
                sys_handler = SysHandlerDetailed()
                file_handler = FileHandlerDetailed()
            case _:
                raise ValueError("Invalid log type. Please select from 'simple' or 'detailed'.")

        return LogBuilder(sys_handler, file_handler)


################# OLD CODE #################


class ISysAndFileLogBuilder(ILogBuilder):
    def __init__(self):
        super().__init__()
        self._sys_handler = None
        self._file_handler = None

    def initiate_logging(self, path: str, name: str):
        self.initiate_sys_logging()
        self.initiate_file_logging(path, name)

    def initiate_sys_logging(self) -> None:
        logging.getLogger().setLevel(logging.DEBUG)
        logging.getLogger().addHandler(self._sys_handler.handler())

    def initiate_file_logging(self, path: str, name: str):
        if '{date}' in name: name.format(date=datetime.date.today())

        if sum([1 for handler in logging.getLogger().handlers if name in str(handler)]) < 1:
            file_handler = self._file_handler.handler(os.path.join(path, name) + ".log")
            logging.getLogger().addHandler(file_handler)


class ISysLogBuilder(ILogBuilder):
    def __init__(self):
        super().__init__()
        self._sys_handler = None
        self._file_handler = None

    def initiate_sys_logging(self):
        logging.getLogger().setLevel(logging.DEBUG)
        logging.getLogger().addHandler(self._sys_handler.handler())


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


# TODO: Implement a Factory class that can make decisions on which loggers to initialise


class LogContext:
    def __init__(self, log_file_path: str):
        self.log_file_path = log_file_path
        self.file_logging = True if log_file_path != "" else False


class LogDirector:
    def __init__(self, builder: ILogBuilder):
        self.builder = builder

    # TODO: This needs to be updated so that the file path is handled elsewhere
    def initiate_logging(self, *args, **kwargs) -> ILogBuilder:
        if not self.builder.get_build_status():

            self.builder.initiate_file_logging(*args, **kwargs)
            self.builder.initiate_sys_logging()

            self.builder.update_build_status()

        else:
            logger.error("You are trying to re-initiate logging. Logging has already been initiated.")

        return self.builder
