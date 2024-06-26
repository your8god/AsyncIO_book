import requests
import asyncio
from concurrent.futures import ThreadPoolExecutor
from util import async_time
from threading import Lock, Thread
from time import sleep

def get_response():
    counter()
    res = requests.get('https://vk.com/im?peers=213956140_103705674')
    return res

async def get_response_async():
    get_response()

progress = 0
lock = Lock()

def counter():
    global progress
    with lock:
        progress += 1


async def print_progress():
    global progress
    while progress < 50:
        print(f'progress: {progress}/50')
        await asyncio.sleep(1.5)


@async_time
async def main1():
    loop = asyncio.get_running_loop()
    with ThreadPoolExecutor(max_workers=35) as pool:
        prog_task = asyncio.create_task(print_progress())
        calls = [loop.run_in_executor(pool, get_response) for _ in range(50)]
        await asyncio.gather(*calls)
        await prog_task


@async_time
async def main2():
    global progress
    progress = 0
    prog_task = asyncio.create_task(print_progress())
    calls = [asyncio.to_thread(get_response) for _ in range(50)]
    await asyncio.gather(*calls)
    await prog_task


@async_time
async def main3():
    global progress
    progress = 0
    prog_task = asyncio.create_task(print_progress())
    await asyncio.gather(*(get_response_async() for _ in range(50)))
    await prog_task


@async_time
async def main4():
    global progress
    progress = 0
    for _ in range(50):
        get_response()


@async_time
async def main5():
    global progress
    progress = 0
    for _ in range(50):
        await get_response_async()


def print_progress_th():
    global progress
    while progress < 50:
        print(f'progress: {progress}/50')
        sleep(1.5)

@async_time
async def main6():
    global progress
    progress = 0
    threads = [Thread(target=get_response) for _ in range(50)]
    progress_thread = Thread(target=print_progress_th)
    progress_thread.start()
    for i in threads:
        i.start()
    progress_thread.join()


@async_time
async def main7():
    global progress
    progress = 0
    with ThreadPoolExecutor(max_workers=50) as pool:
        res = pool.submit(print_progress_th)
        ress = [pool.submit(get_response) for _ in range(50)]
        res.result()


async def main():
    await main1()
    print()
    await main2()
    print()
    await main3()
    print()
    await main4()
    print()
    await main5()
    print()
    await main6()
    print()
    await main7()

asyncio.run(main())