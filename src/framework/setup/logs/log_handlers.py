import logging
import sys
from abc import ABC, abstractmethod
from logging import LogRecord
from typing import Callable

from framework.setup.logs.log_formaters import ColourfulSysFormatter, MutedSysFormatter


class ILogHandler(ABC):

    def __init__(self, log_format: str):
        self.log_format = log_format

    @abstractmethod
    def handler(self) -> logging.FileHandler:
        pass

    @staticmethod
    def build_handler_filters(handler: str) -> Callable[[LogRecord], bool]:
        def handler_filter(record: logging.LogRecord) -> bool:
            if hasattr(record, 'block'):
                if handler in record.block:
                    return False
            return True

        return handler_filter


class FileHandler(ILogHandler):

    def __init__(self, log_format: str, log_file_path: str):
        super().__init__(log_format)
        self.formatter = logging.Formatter(self.log_format)
        self.log_file_path = log_file_path
        self.initiate_file_logger = True if log_file_path != "" else False

    def handler(self) -> logging.FileHandler:
        fl_handler = logging.FileHandler(self.log_file_path, 'w+')
        fl_handler.setFormatter(self.formatter)
        fl_handler.setLevel(logging.DEBUG)
        fl_handler.addFilter(self.build_handler_filters('file'))
        return fl_handler


class SysHandler(ILogHandler):

    def __init__(self, log_format: str):
        super().__init__(log_format)
        self.formatter = MutedSysFormatter(self.log_format)
        self.sys_handler = None

    def handler(self) -> logging.StreamHandler:
        sys_handler = logging.StreamHandler(sys.stdout)
        sys_handler.setFormatter(self.formatter)
        sys_handler.setLevel(logging.DEBUG)
        sys_handler.addFilter(self.build_handler_filters('console'))
        self.sys_handler = sys_handler
        return sys_handler

    def mute_colours(self):
        self.formatter = MutedSysFormatter(self.log_format)
        self.sys_handler.setFormatter(MutedSysFormatter(self.log_format))

    def unmute_colours(self):
        self.formatter = ColourfulSysFormatter(self.log_format)
        self.sys_handler.setFormatter(ColourfulSysFormatter(self.log_format))


class LogHandlerContext:
    def __init__(self, log_file_path: str, log_type: str):
        self.log_file_path = log_file_path
        self.log_type = log_type


class LogHandlerFactory:

    def __init__(self, context: LogHandlerContext):
        self.context = context

    def create_handlers(self) -> tuple[SysHandler, FileHandler]:
        match self.context.log_type:
            case 'simple':
                log_format = "%(message)s"
            case 'detailed':
                log_format = "[%(asctime)s] %(levelname)s [%(name)s.%(module)s.%(funcName)s: %(lineno)d] %(message)s"
            case _:
                raise ValueError(f"Invalid log type: {self.context.log_type}. "
                                 f"Please select from 'simple' or 'detailed'.")

        return SysHandler(log_format), FileHandler(log_format, self.context.log_file_path)
