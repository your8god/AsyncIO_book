import asyncio
from functools import wraps
import time

def async_time(f):
    @wraps(f)
    async def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        print(f'{f.__name__} is starting')
        try:
            return await f(*args, **kwargs)
        finally:
            print(f'{f.__name__} is ending. Total time = {round(time.perf_counter() - start_time, 5)}')
    return wrapper