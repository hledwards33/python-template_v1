import logging
import math


class LogStructures:

    def __init__(self, log_format: str):
        self.log_format = log_format

    def expected_file_format(self) -> None:
        for handler in logging.getLogger().handlers:
            if isinstance(handler, logging.FileHandler):
                fl_format = logging.Formatter(self.log_format)
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
