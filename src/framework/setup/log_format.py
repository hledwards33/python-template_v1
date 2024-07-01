import datetime
import logging
import math
import os
import re
import sys


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

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def headers(message: str):
    line_length = 75
    line_num_start = line_length - math.ceil(len(message) / 2)
    line_num_end = line_num_start if line_num_start % 2 == 0 else line_num_start + 1
    lines_start = ''.join(['-' for _ in range(line_num_start)])
    lines_end = ''.join(['-' for _ in range(line_num_end)])
    print()
    print(lines_start + ' ' + message + ' ' + lines_end)
    print()

    simple_file_format()
    logging.info("", extra={'block': ['console']})
    logging.info(lines_start + ' ' + message + ' ' + lines_end + "\n", extra={'block': ['console']})
    detailed_file_format()


def no_format(message: str):
    simple_file_format()
    logging.info(message, extra={'block': ['console']})
    print(message)
    detailed_file_format()


def detailed_file_format():
    for handler in logging.getLogger().handlers:
        if isinstance(handler, logging.FileHandler):
            fl_format = logging.Formatter("[%(asctime)s] %(levelname)s [%(name)s.%(module)s.%(funcName)s:"
                                          " %(lineno)d] %(message)s")
            handler.setFormatter(fl_format)


def simple_file_format():
    for handler in logging.getLogger().handlers:
        if isinstance(handler, logging.FileHandler):
            handler.setFormatter(logging.Formatter('%(message)s'))


def lines():
    output = "".join(["-" for _ in range(75)])

    print(output)


def create_logging_file_handler_detailed(path: str):
    fl_handler = logging.FileHandler(path, 'w+')
    fl_format = logging.Formatter("[%(asctime)s] %(levelname)s [%(name)s.%(module)s.%(funcName)s:"
                                  " %(lineno)d] %(message)s")
    fl_handler.setFormatter(fl_format)
    fl_handler.setLevel(logging.DEBUG)
    fl_handler.addFilter(build_handler_filters('file'))
    return fl_handler


def create_logging_file_handler_simple(path: str):
    fl_handler = logging.FileHandler(path, 'w+')
    fl_format = logging.Formatter("%(message)s")
    fl_handler.setFormatter(fl_format)
    fl_handler.setLevel(logging.DEBUG)
    fl_handler.addFilter(build_handler_filters('file'))
    return fl_handler


def create_logging_file(file_handler, path: str, name: str, data_name: str = None):
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


def create_logging_sys_handler_detailed():
    sys_handler = logging.StreamHandler(sys.stdout)
    cn_format = CustomFormatter(
        "[%(asctime)s] %(levelname)s [%(name)s.%(module)s.%(funcName)s: %(lineno)d] %(message)s")
    sys_handler.setFormatter(cn_format)
    sys_handler.setLevel(logging.DEBUG)
    sys_handler.addFilter(build_handler_filters('console'))
    return sys_handler


def create_logging_sys_handler_simple():
    sys_handler = logging.StreamHandler(sys.stdout)
    cn_format = CustomFormatter("%(message)s")
    sys_handler.setFormatter(cn_format)
    sys_handler.setLevel(logging.DEBUG)
    sys_handler.addFilter(build_handler_filters('console'))
    return sys_handler


def remove_handler(name):
    name = re.sub("\{.*?\}", "", name)

    for handler in logging.getLogger().handlers:
        if name in str(handler):
            logging.getLogger().removeHandler(handler)


def build_handler_filters(handler: str):
    def handler_filter(record: logging.LogRecord):
        if hasattr(record, 'block'):
            if handler in record.block:
                return False
        return True

    return handler_filter


def initiate_logger():
    logging.getLogger().setLevel(logging.DEBUG)
    logging.getLogger().addHandler(create_logging_sys_handler_detailed())
