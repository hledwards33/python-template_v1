import logging
import math
import os
import re
from datetime import datetime

from framework.setup.logs.log_handlers import FileHandler, SysHandler
from framework.setup.structures.meta_classes.singleton import ThreadSafeSingletonABCMeta


class ILogBuilder(metaclass=ThreadSafeSingletonABCMeta):
    __build_status: bool = False  # Initiating a private class variable

    def __init__(self, sys_handler: SysHandler, file_handler: FileHandler):
        self._sys_handler = sys_handler
        self._file_handler = file_handler

    def update_build_status(self):
        self.__build_status = not self.__build_status

    def get_build_status(self) -> bool:
        return self.__build_status

    def initiate_logging(self):
        self.initiate_sys_logging()
        if self._file_handler.initiate_file_logger: self.initiate_file_logging()
        self.update_build_status()

    def initiate_sys_logging(self) -> None:
        logging.getLogger().setLevel(logging.DEBUG)
        logging.getLogger().addHandler(self._sys_handler.handler())

    def initiate_file_logging(self):
        name = os.path.split(self._file_handler.log_file_path)[-1]
        if '{date}' in name: name.format(date=datetime.date.today())

        if sum([1 for handler in logging.getLogger().handlers if name in str(handler)]) < 1:
            file_handler = self._file_handler.handler()
            logging.getLogger().addHandler(file_handler)

    def expected_file_format(self) -> None:
        for handler in logging.getLogger().handlers:
            if isinstance(handler, logging.FileHandler):
                fl_format = logging.Formatter(self._file_handler.log_format)
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
