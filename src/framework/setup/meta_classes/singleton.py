import threading
from abc import ABCMeta


# class ThreadSafeSingleton(type):
#     """This is a lazy loading implementation of the Singleton Pattern"""
#     _instances: dict = {}
#     _lock: threading.Lock = threading.Lock()
#
#     def __call__(cls, *args, **kwargs):
#         with cls._lock:
#             if cls not in cls._instances:
#                 cls._instances[cls] = super(ThreadSafeSingleton, cls).__call__(*args, **kwargs)
#             return cls._instances[cls]

class ThreadSafeSingletonMeta(type):
    _instances = {}  # Dictionary to hold the instance reference for each class.
    _lock = threading.Lock()  # A lock to ensure thread-safe singleton instantiation.

    def __call__(cls, *args, **kwargs):
        # Acquire the lock to make sure that only one thread can enter this block at a time.
        with cls._lock:
            # Check if the instance already exists for the class.
            if cls not in cls._instances:
                # If not, create the instance and store it in the _instances dictionary.
                cls._instances[cls] = super().__call__(*args, **kwargs)
        # Return the instance.
        return cls._instances[cls]


# This metaclass combines the features of SingletonMeta and ABCMeta.
class ThreadSafeSingletonABCMeta(ABCMeta, ThreadSafeSingleton):
    def __new__(cls, name, bases, namespace):
        # Create a new class using the combined metaclasses.
        return super().__new__(cls, name, bases, namespace)
