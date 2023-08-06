import time
from contextlib import contextmanager

from functools import wraps


class Potency:
    def __init__(self):
        self.start = time.process_time()
        self.end = self.start

    def record(self):
        last = self.start

        self.end = time.process_time()
        self.start = self.end

        return self.end - last


@contextmanager
def timeblock():
    yield Potency()


def timefunc(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.process_time()
        r = func(*args, **kwargs)
        end = time.process_time()
        print(f'{func.__module__}.{func.__name__} : {(end - start):.2f}')
        return r

    return wrapper
