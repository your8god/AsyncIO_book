import asyncio

async def delay(s, name='def'):
    print(f'task {name} is begining')
    await asyncio.sleep(s)
    print(f'task {name} is finished')