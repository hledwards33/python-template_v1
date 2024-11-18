import threading


class SingletonMeta(type):
    _instances: dict = {}
    _lock: threading.Lock = threading.Lock()

    def __init__(cls):
        cls._instances[cls] = super().__init__(cls)

    def __new__(cls):
        return cls._instances[cls]
