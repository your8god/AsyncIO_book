import asyncio
import random
from util import delay, async_time

async def test(name, locker):
    async with locker:
        print(name, 'start')
        await asyncio.sleep(random.randint(0, 3))
        print(name, 'end')


async def main1():
    locker = asyncio.Lock()
    tasks = [test(i, locker) for i in range(5)]
    await asyncio.gather(*tasks)


async def main2():
    locker = asyncio.Semaphore(2)
    tasks = [test(i, locker) for i in range(10)]
    await asyncio.gather(*tasks)


@async_time
async def action(event, name):
    print(f'{name} is waiting event')
    await event.wait()
    print(f'{name} is completed')
    event.clear()


async def new_delay(s, event):
    await delay(s, 'delay')
    event.set()
    print('Event is released!')


@async_time
async def main3():
    event = asyncio.Event()
    task1 = asyncio.create_task(action(event, 1))
    delay_task = asyncio.create_task(new_delay(5, event))
    await task1


async def cond(locker, name):
    async with locker:
        await asyncio.sleep(random.randint(1, 2))
        print(name, 'is inside!')
        await locker.wait()
        print(name, 'is outside!')


async def gener():
    for _ in range(7):
        await asyncio.sleep(0.1)
        yield random.randint(1, 8)


async def put_queue(queue):
    async for i in gener():
        await queue.put(i)
        #queue.put_nowait(i)


async def get_queue(queue, locker):
    async with locker:
        await asyncio.sleep(random.randint(3, 5))
        while not queue.empty():
            print(queue.get_nowait())
            #await asyncio.sleep(1)
            queue.task_done()
        locker.notify_all()


async def main4():
    locker = asyncio.Condition()
    queue = asyncio.Queue(4)
    tasks = [asyncio.create_task(cond(locker, i)) for i in range(1, 4)]
    tasks.extend([asyncio.create_task(put_queue(queue)), 
                  asyncio.create_task(get_queue(queue, locker)), 
                  asyncio.create_task(queue.join())])
    await asyncio.gather(*tasks)
    print('END')
    print(queue)
    for task in tasks:
        print(task.get_name(), task.done())


async def main():
    #await main1()
    #await main2()
    #await main3()
    await main4()


asyncio.run(main())