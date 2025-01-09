import logging
import os
import re

from framework.setup.logs.log_handlers import FileHandler, SysHandler
from framework.setup.structures.meta_classes.singleton import ThreadSafeSingletonABCMeta


class LogBuilder(metaclass=ThreadSafeSingletonABCMeta):
    __build_status: bool = False  # build status is a private class variable

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

        if sum([1 for handler in logging.getLogger().handlers if name in str(handler)]) < 1:
            file_handler = self._file_handler.handler()
            logging.getLogger().addHandler(file_handler)

    def terminate_logging(self, name) -> None:
        name = re.sub(r"\{.*?}", "", name)

        for handler in logging.getLogger().handlers:
            if name in str(handler):
                logging.getLogger().removeHandler(handler)

        self.update_build_status()
