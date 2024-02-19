import asyncio
from util import delay, async_time

@async_time
async def main():
    tasks = asyncio.as_completed([delay(10, 1), delay(3, 2), delay(1, 3)], timeout=3.5)
    for it in tasks:
        try:
            await it
        except asyncio.TimeoutError:
            print('Timeout')

    for task in asyncio.tasks.all_tasks():
        print(task)
    

@async_time
async def main():
    tasks = [
        asyncio.wait_for(asyncio.create_task(delay(10, 1)), 5),
        asyncio.wait_for(asyncio.create_task(delay(3, 2)), 5),
        asyncio.wait_for(asyncio.create_task(delay(4, 3)), 5),
        asyncio.wait_for(asyncio.create_task(delay(4, 4)), 1),     
    ]

    res = await asyncio.gather(*tasks, return_exceptions=True)
    print(res)


@async_time
async def main():
    pending = [
        asyncio.create_task(delay(3, 1)),
        asyncio.create_task(delay(6, 2)),
        asyncio.create_task(delay(4, 3)),
        asyncio.create_task(delay(2, 4))
    ]

    '''while pending:
        done, pending = await asyncio.wait(pending, return_when='FIRST_COMPLETED')
        print(f'Done size {len(done)}')
        print(f'Pending size {len(pending)}')'''
    
    done, pending = await asyncio.wait(pending, timeout=3.5)
    print(f'Done size {len(done)}')
    print(f'Pending size {len(pending)}')

    for task in pending:
        print(task, task.get_name())
    print()

    for task in pending:
        task.cancel()

    for task in pending:
        print(task, task.get_name())

asyncio.run(main())


