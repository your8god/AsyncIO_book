import asyncio
from time import perf_counter as pc
from util import delay, async_time


async def my_range(s):
    print('start range')
    for i in range(s):
        print('start waiting...')
        await asyncio.sleep(4)
        print('...stop waiting')
    print('stop range')


async def main():
    task1 = asyncio.create_task(delay(2, 1))
    task2 = asyncio.create_task(delay(1, 2))
    await my_range(2)
    #await task1
    #await task2

async def main():
    task1 = asyncio.create_task(delay(3, 'T1'))
    start_time = pc()
    #await asyncio.create_task(delay(0.00001, ''))

    while not task1.done():
        await asyncio.sleep(0)
        current_time = pc() - start_time
        print(f'now is {current_time}')
        if current_time > 5:
            task1.cancel('too long')

    try:
        await task1
    except asyncio.CancelledError as e:
        print(e.args)
 

@async_time
async def cpu_bound():
    counter = 0
    for i in range(100000000):
        counter += 1
    return counter

@async_time
async def main():
    delay_task = asyncio.create_task(delay(1, 'DD')) #очевидно, что этот вариант быстрее, тк таска первая в очереди
    task1 = asyncio.create_task(cpu_bound())
    task2 = asyncio.create_task(cpu_bound())
    #delay_task = asyncio.create_task(delay(4, 'DD'))
    await delay_task
    await task1
    await task2

asyncio.run(main())