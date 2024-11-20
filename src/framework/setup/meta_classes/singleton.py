import threading


class ThreadSafeSingleton(type):
    """This is a lazy loading implementation of the Singleton Pattern"""
    _instances: dict = {}
    _lock: threading.Lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                cls._instances[cls] = super(ThreadSafeSingleton, cls).__call__(*args, **kwargs)
            return cls._instances[cls]
