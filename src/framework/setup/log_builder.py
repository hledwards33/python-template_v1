import threading

from log_handlers import ILogHandler, IFileHandler, ISysHandler, SysHandlerSimple


class SingletonMeta(type):
    """This is an eager implementation of the Singleton Pattern"""
    _instances: dict = {}
    _lock: threading.Lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                cls._instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
            return cls._instances[cls]


class LogBuilder(metaclass=SingletonMeta):

    def __init__(self, SysHandler: ISysHandler = SysHandlerSimple, FileHandler: IFileHandler = None):
        self._sys_handler = SysHandler
        self._file_handler = FileHandler

    def add_handler(self, Handler: ILogHandler):
        if isinstance(Handler, IFileHandler):
            self._file_handler = Handler

        elif isinstance(Handler, ISysHandler):
            self._sys_handler = Handler
