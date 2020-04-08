'''
Copyright (C) 2020 Link Shortener Authors
Licensed under the MIT (Expat) License. See the LICENSE file found in the
top-level directory of this distribution.
'''
from asyncio import get_event_loop

from aiomysql import connect, create_pool
# from aiomysql.sa import create_engine

# from sqlalchemy.sql import select

from json import dumps

from sanic import Sanic, response
from sanic.response import json


app = Sanic(__name__)


@app.listener('before_server_start')
async def initialise_db(app, loop):
    pool = await create_pool(
        host='db',
        port=3306,
        user='user',
        password='password',
        db='db',
        loop=loop
    )
    async with pool.acquire() as conn:
        db_cursor = await conn.cursor()

        await db_cursor.execute(
            'CREATE TABLE IF NOT EXISTS links (endpoint TEXT, url TEXT)'
        )
        query = 'INSERT INTO links (endpoint, url) VALUE (%s, %s)'
        data = [
            ('pomuzemesi', 'https://staging.pomuzeme.si'),
            ('vlk', 'http://www.vlk.cz'),
            ('kodex', 'https://github.com/Applifting/culture'),
            ('meta', 'https://github.com/Applifting/link-shortener')
        ]
        await db_cursor.executemany(query, data)
        await conn.commit()

        await db_cursor.close()
        conn.close()


@app.route('/api/links', methods=['GET'])
async def get_links(request):
    try:
        loop = get_event_loop()
        pool = await create_pool(
            host='db',
            port=3306,
            user='user',
            password='password',
            db='db',
            loop=loop
        )
        async with pool.acquire() as conn:
            db_cursor = await conn.cursor()

            await db_cursor.execute('SELECT * FROM links')
            qs = await db_cursor.fetchall()
            data = dumps(qs)

            await db_cursor.close()
            conn.close()

            return json(data, status=200)

    except Exception as error:
        print(error)
        return json({'message': 'getting links failed'}, status=500)


@app.route('/<link_endpoint>')
async def redirect_link(request, link_endpoint):
    try:
        loop = get_event_loop()
        # conn = await connect(
        #     host='db',
        #     port=3306,
        #     user='user',
        #     password='password',
        #     db='db',
        #     loop=loop
        # )
        # db_cursor = await conn.cursor()
        pool = await create_pool(
            host='db',
            port=3306,
            user='user',
            password='password',
            db='db',
            loop=loop
        )
        async with pool.acquire() as conn:
            db_cursor = await conn.cursor()

            query = 'SELECT * FROM links WHERE endpoint = %s'
            value = (link_endpoint,)
            await db_cursor.execute(query, value)
            result = await db_cursor.fetchall()

            url = result[0][1]
            return response.redirect(url)

    except Exception as error:
        print(error)
        return json({'message': 'link does not exist'}, status=400)


if (__name__ == '__main__'):
    app.run(host='0.0.0.0', port=8000)
