import asyncio

async def main():
    proc = await asyncio.create_subprocess_exec('ls', '-l')
    #print(proc.pid)
    #print(await proc.wait())
    await proc.wait()

asyncio.run(main())