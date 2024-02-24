import asyncio
import asyncpg
from random import sample, randint


def read():
    with open('/Users/bogdan/Documents/AsyncIO/postgers/common_words.txt', encoding='utf-8', newline='\n') as f:
        return f.readlines()

    
def gener_insert_values(mode):
    values = read()
    if mode == 0:
        return [(i, str.strip(v)) for i, v in enumerate(sample(values, 100), 3)]
    elif mode == 1:
        return [
            ('-'.join(str.strip(i) for i in sample(values, randint(2, 5))), randint(1, 102)) 
            for _ in range(100)
        ]
    else:
        return [
            (randint(1, 100), randint(1, 3), randint(1, 11)) for _ in range(100000)
        ]
    

async def insert_into_brand(connection):
    values = gener_insert_values(0)
    await connection.execute('DELETE FROM brand WHERE brand_id > 2;')

    insert_query = 'INSERT INTO brand VALUES ($1, $2)'
    print(await connection.executemany(insert_query, values))
    res = await connection.fetch('SELECT * FROM brand')
    for i in res:
        print(i['brand_id'], i['brand_name'])


async def insert_into_color(connection):
    query = " \
        INSERT INTO product_color (product_color_name) VALUES \
        ('Green'), ('Grey'), ('Red'), ('Orange'), ('Yellow'), ('Sky'), ('White'), ('Purpel'), ('Pink'); \
    "

    await connection.execute(query)
    for i in await connection.fetch('SELECT * FROM product_color;'):
        print(i['product_color_id'], i['product_color_name'])


async def insert_into_product(connection):
    values = gener_insert_values(1)  
    insert_query = 'INSERT INTO product (product_name, brand_id) VALUES ($1, $2)'
    await connection.executemany(insert_query, values)
    res = await connection.fetch('SELECT * FROM product;')
    for i in res:
        print(
            i['product_id'],
            i['product_name'],
            i['brand_id']
        )


async def insert_into_sku(connection):
    values = gener_insert_values(2)
    insert_query = '''
        INSERT INTO sku (product_id, product_size_id, product_color_id) VALUES ($1, $2, $3)
    '''
    await connection.executemany(insert_query, values)
    res = await connection.fetch('SELECT * FROM sku LIMIT 10 OFFSET 90000;')
    for i in res:
        print(i['sku_id'], i['product_id'], i['product_size_id'], i['product_color_id'])

    
async def main():
    connection = await asyncpg.connect(
        host='127.0.0.1',
        port=5432,
        user='postgres',
        database='products'
        #password='password' 
    )

    #await insert_into_brand(connection)
    #await insert_into_color(connection)
    #await asyncio.sleep(5)
    #await insert_into_product(connection)
    #await insert_into_sku(connection)

    await connection.close()

asyncio.run(main())