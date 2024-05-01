import logging
import sys

import numpy as np
import math


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
    print(lines_start + ' ' + message + ' ' + lines_end)
    logging.info(message)


logging.getLogger().setLevel(logging.DEBUG)

sys_handler = logging.StreamHandler(sys.stdout)
cn_format = CustomFormatter("[%(asctime)s] %(levelname)s [%(name)s.%(module)s.%(funcName)s: %(lineno)d] %(message)s")
sys_handler.setFormatter(cn_format)
sys_handler.setLevel(logging.DEBUG)

logging.getLogger().addHandler(sys_handler)
