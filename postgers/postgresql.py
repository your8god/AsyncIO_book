import asyncpg
import asyncio
from script_for_db import *


async def create_table():
    connection = await asyncpg.connect(
        host='127.0.0.1',
        port=5432,
        user='postgres',
        database='products',
        password='password' #??? may be it should be deleted later
    )
    #version = connection.get_server_version()
    #print(f'Version: {version}')
    
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
    connection = await asyncpg.connect(
        host='127.0.0.1',
        port=5432,
        user='postgres',
        database='products'
    )

    res1 = await connection.fetch('SELECT * FROM product_size;')
    res2 = await connection.fetch('SELECT * FROM product_color;')
    for line in res2:
        print(line['product_color_id'], line['product_color_name'])
    print()
    for line in res1:
        print(line['product_size_id'], line['product_size_name'])

    await connection.close()


async def main():
    #await create_table()
    await select()

asyncio.run(main())