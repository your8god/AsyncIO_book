import asyncio
from util import async_time
from util import delay
import threading
import time
import aiofiles
from functools import wraps
import aiofiles.os

def testing(name=''):
    def decor(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            print(f'START TEST: {name}')
            res = f(*args, **kwargs)
            print(f'END TEST: {name}\n')
            return res
        return wrapper
    return decor



def sync_read(name):
    with open(name, 'rb') as f:
        content = f.readlines()
        print(f'{name} is ready')
    return content

def sleep_f(i):
    print('im asleep', i)
    time.sleep(2)
    print('im awake', i)

@async_time
async def tt():
    print('using treads')
    tasks = [asyncio.to_thread(sync_read, str(i)) for i in range(3)]
    tasks.extend([asyncio.to_thread(sleep_f, i) for i in range(3)])
    res = await asyncio.gather(*tasks)


@testing(name='without aiofiles, using threads')
def test1():
    '''DOC TEST1'''
    print('without threads')
    start = time.perf_counter()
    for i in range(3):
        sync_read(str(i))
        sleep_f(i)
    print(time.perf_counter() - start, '\n')

    print('read without async???')
    start = time.perf_counter()
    threads = [threading.Thread(target=sync_read, args=(str(i),)) for i in range(3)]
    threads.extend([threading.Thread(target=sleep_f, args=(i,)) for i in range(3)])
    [t.start() for t in threads]
    [t.join() for t in threads]
    print(time.perf_counter() - start, '\n')

    asyncio.run(tt())


async def async_read(name):
    async with aiofiles.open(name, 'rb') as f:
        content = await f.readlines()
        print(f'{name} is ready')
    return content

@async_time
async def f():
    tasks = [asyncio.create_task(async_read(str(i))) for i in range(6)]
    await asyncio.gather(*tasks, asyncio.sleep(10))

@testing(name='with aiofiles, using tasks')
def test2():
    async def main():
        print('without threads')
        start = time.perf_counter()
        for i in range(6):
            sync_read(str(i))
        await asyncio.sleep(10)
        print(time.perf_counter() - start, '\n')

        await f()

    asyncio.run(main())

#print(test1.__name__, test1.__doc__)
test1()
test2()