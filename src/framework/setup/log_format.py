import datetime
import logging
import math
import os
import sys


class CustomFormatter(logging.Formatter):
    """Logging colored formatter, adapted from https://stackoverflow.com/a/56944256/3638629"""

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

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def headers(message: str):
    line_num = 75
    line_num_start = line_num - math.ceil(len(message) / 2)
    line_num_end = line_num_start if line_num_start % 2 == 0 else line_num_start + 1
    lines_start = ''.join(['-' for _ in range(line_num_start)])
    lines_end = ''.join(['-' for _ in range(line_num_end)])
    print()
    print(lines_start + ' ' + message + ' ' + lines_end)
    print()
    logging.info(message + ".")


def lines():
    output = "".join(["-" for _ in range(75)])

    print(output)


def create_logging_file_handler(path: str):
    fl_handler = logging.FileHandler(path, 'w+')
    fl_format = logging.Formatter("[%(asctime)s] %(levelname)s [%(name)s.%(module)s.%(funcName)s:"
                                  " %(lineno)d] %(message)s")
    fl_handler.setFormatter(fl_format)
    fl_handler.setLevel(logging.DEBUG)
    return fl_handler


def create_logging_file(path: str, name: str):
    if '{date}' in name:
        name = name.format(date=str(datetime.date.today()))

    if sum([1 for handler in logging.getLogger().handlers if name in str(handler)]) < 1:
        fil_handler = create_logging_file_handler(os.path.join(path, name) + ".log")
        logging.getLogger().addHandler(fil_handler)


def create_logging_sys_handler():
    sys_handler = logging.StreamHandler(sys.stdout)
    cn_format = CustomFormatter(
        "[%(asctime)s] %(levelname)s [%(name)s.%(module)s.%(funcName)s: %(lineno)d] %(message)s")
    sys_handler.setFormatter(cn_format)
    sys_handler.setLevel(logging.DEBUG)
    return sys_handler


logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger().addHandler(create_logging_sys_handler())
