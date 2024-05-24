import asyncio
from aiohttp import web
from aiohttp.web_app import Application
from aiohttp.web_request import Request
from aiohttp.web_response import Response
import asyncpg
from asyncpg import Record
from asyncpg.pool import Pool
import json

routes = web.RouteTableDef()
DB_KEY = 'database'

async def create_db_pool(app):
    print('Create connect pool')
    pool = await asyncpg.create_pool(
        host='127.0.0.1',
        port=5432, 
        user='postgres',
        database='products',
        min_size=2,
        max_size=5
    )
    app[DB_KEY] = pool

async def destroy_db_pool(app):
    print('Destroy connect pool')
    await app[DB_KEY].close()

@routes.get('/products')
async def brands(request):
    query = 'SELECT sku_id, product_name FROM sku JOIN product USING(product_id)'
    results = await request.app[DB_KEY].fetch(query)
    d = [dict(brand) for brand in results]
    total = await request.app[DB_KEY].fetch('SELECT COUNT(*) FROM sku')    
    d.append(dict(total[0]))
    return web.json_response(d)

@routes.get('/products/{id}')
async def brands_id(request):
    try:
        s_id = int(request.match_info['id'])
        query = f'SELECT sku_id, product_name, brand_name, product_color_name, product_size_name \
            FROM product JOIN sku USING(product_id) \
                JOIN brand USING(brand_id)\
                    JOIN product_color USING(product_color_id)\
                        JOIN product_size USING(product_size_id) WHERE sku_id = {s_id};'
        results = await request.app[DB_KEY].fetch(query)
        if not results:
            results = await request.app[DB_KEY].fetch('SELECT COUNT(*) FROM sku')    
        d = dict(results[0])
        return web.json_response(d)
    except:
        web.json_response({'Error' : ''})


@routes.post('/products/add')
async def add_favourites(request):
    SKU_ID = 'sku_id'
    USER_ID = 'user_id'

    body = await request.json()
    if SKU_ID in body and USER_ID in body:
        db = request.app[DB_KEY]
        await db.execute('INSERT INTO favourit(user_id, sku_id) VALUES($1, $2);', int(body[USER_ID]), 
                         int(body[SKU_ID]))
        return web.Response(status=201)
    else:
        return web.Response(status=403)
    

@routes.get('/user/{id}')
async def get_user_list(request):
    try:
        s_id = int(request.match_info['id'])
        print(s_id)
        query = f'''SELECT sku_id, product_name, brand_name, product_color_name, product_size_name FROM sku 
JOIN favourit USING(sku_id)
JOIN product USING(product_id)
JOIN brand USING(brand_id)
JOIN product_color USING(product_color_id)
JOIN product_size USING(product_size_id) WHERE user_id = {s_id};'''
        results = await request.app[DB_KEY].fetch(query)
        if not results:
            results = await request.app[DB_KEY].fetch('SELECT COUNT(*) FROM favourit')    
        d = [dict(brand) for brand in results]
        return web.json_response(d)
    except:
        web.json_response({'Error' : ''})



app = web.Application()
app.on_startup.append(create_db_pool)
app.on_cleanup.append(destroy_db_pool)

app.add_routes(routes)
web.run_app(app)