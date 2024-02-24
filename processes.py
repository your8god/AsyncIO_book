from concurrent.futures import ProcessPoolExecutor
import asyncio
import multiprocessing
from functools import partial
from util import async_time


def counting(name):
    print(f'{name} is started')
    counter = 0
    for i in range(100000000):
        counter += 1
    print(f'{name} is finished')
    return name


@async_time
async def main1():
    loop = asyncio.get_running_loop()
    with ProcessPoolExecutor() as pool:
        calls = [loop.run_in_executor(pool, partial(counting, i)) for i in range(1, 8)]
        res = ''
        for i in asyncio.as_completed(calls): 
            res += '{} '.format(await i)
        print(res)

@async_time
async def main2():
    task1 = multiprocessing.Process(target=counting, args=(1, ))
    task2 = multiprocessing.Process(target=counting, args=(2, ))
    task1.start()
    task2.start()
    task1.join()
    task2.join()


@async_time
async def main3():
    with multiprocessing.Pool() as pool:
        task1 = pool.apply(counting, args=(1, ))
        task2 = pool.apply(counting, args=(2, ))


@async_time
async def main4():
    with multiprocessing.Pool() as pool:
        task1 = pool.apply_async(counting, args=(1, ))
        task2 = pool.apply_async(counting, args=(2, ))
        print(task1.get())
        print(task2.get())


@async_time
async def main5():
    with ProcessPoolExecutor() as pool:
        for i in pool.map(counting, (1, 2)):
            print(i)


shared_var = multiprocessing.Value('d', 0)

def init_shared_val(val):
    global shared_var
    shared_var = val

def inc():
    #with shared_var.get_lock():
        for _ in range(100000):
            shared_var.value += 1
        print(shared_var.value)


@async_time
async def main6():
    val = multiprocessing.Value('d', 0)
    loop = asyncio.get_running_loop()
    with ProcessPoolExecutor(initializer=init_shared_val, initargs=(val, )) as pool:
        calls = [loop.run_in_executor(pool, inc) for _ in range(7)]
        await asyncio.gather(*calls)
        print(val.value)


@async_time
async def main():
    #await main1()
    #await main2()
    #await main3()
    #await main4()
    #await main5()
    await main6()


if __name__ == '__main__':
    asyncio.run(main(), debug=False)