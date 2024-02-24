import sys
sys.path.append('/Users/bogdan/Documents/AsyncIO/')


import asyncpg
import asyncio
from script_for_db import *
from random import randint
from util import async_time


async def get_connection():
    connection = await asyncpg.connect(
        host='127.0.0.1',
        port=5432,
        user='postgres',
        database='products'
        #password='password' 
    )
    return connection


async def create_table():
    connection = get_connection()
    
    statements = [CREATE_BRAND_TABLE,
                  CREATE_PRODUCT_TABLE,
                  CREATE_PRODUCT_COLOR_TABLE,
                  CREATE_PRODUCT_SIZE_TABLE,
                  CREATE_SKU_TABLE,
                  SIZE_INSERT,
                  COLOR_INSERT]
    
    print('Database is creating...')
    for i in statements:
        print(await connection.execute(i))
    print('...Database was created')
    
    await connection.close()


async def select():
    connection = await get_connection()

    res1 = await connection.fetch('SELECT * FROM product_size;')
    res2 = await connection.fetch('SELECT * FROM product_color;')
    for line in res2:
        print(line['product_color_id'], line['product_color_name'])
    print()
    for line in res1:
        print(line['product_size_id'], line['product_size_name'])

    await connection.close()


async def insert():
    connection = await get_connection()
    res = await connection.execute("INSERT INTO brand (brand_name) VALUES ('Levis'), ('Seven');")
    print(res)

    for i in await connection.fetch('SELECT * FROM brand;'):
        print(i['brand_id'], i['brand_name'])


async def db_delay(query, time, connection):
    print("The query is executing:\n ", query, '\n Time: ', time)
    await asyncio.sleep(time)
    res = await connection.fetchrow(query)
    #print(res)
    return res


async def test():
    connection = await get_connection()
    queries = ['SELECT * FROM product_size;',
               'SELECT * FROM product_color;',
               'SELECT * FROM brand;']
    
    my_tasks = [db_delay(i, randint(1, 6), connection) for i in queries]

    #1
    #res = await asyncio.gather(*my_tasks, 
    #                           return_exceptions=True)
    #for i in res:
    #    print(i)
    #2
    #tasks = asyncio.as_completed(my_tasks, timeout=3)
    #for i in tasks:
    #    print(await i)
    #3
    pending = [asyncio.create_task(i) for i in my_tasks]
    while pending:
        done, pending = await asyncio.wait(pending, return_when='FIRST_COMPLETED')
        for i in done:
            print("It was an exception!" if i.exception() else i.result())

    #done, pending = await asyncio.wait(pending, timeout=3.0) 
    #for i in done:
    #    print("It was an exception!" if i.exception() else i.result())

    #for i in pending:
    #    i.cancel()

    #done, pending = await asyncio.wait(pending, return_when='FIRST_EXCEPTION') 
    #for i in done:
    #    print("It was an exception!" if i.exception() else i.result())

    #for i in pending:
    #    i.cancel()

    await connection.close()


@async_time
async def test_query(pool):
    async with pool.acquire() as connection:
        await asyncio.sleep(2)
        await connection.fetch('SELECT * FROM sku ORDER BY product_id LIMIT 50')


@async_time
async def pool_test():
    pool = await asyncpg.create_pool(
        host='127.0.0.1',
        port=5432, 
        user='postgres',
        database='products',
        min_size=2,
        max_size=5
    )

    await asyncio.gather(
        test_query(pool),
        test_query(pool),
        test_query(pool),
        test_query(pool),
        test_query(pool)
    )


@async_time
async def main():
    #await create_table()
    #await select()
    #await insert()
    #await test()
    await pool_test()


print(__name__)
if __name__ == '__main__':
    asyncio.run(main())