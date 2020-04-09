'''
Copyright (C) 2020 Link Shortener Authors
Licensed under the MIT (Expat) License. See the LICENSE file found in the
top-level directory of this distribution.
'''
from asyncio import get_event_loop

from aiomysql import create_pool
from aiomysql.sa import create_engine

from sqlalchemy import MetaData, Table, Column, String
from sqlalchemy.sql import select

from json import dumps

from sanic import Sanic, response
from sanic.response import json


app = Sanic(__name__)

metadata = MetaData()
table = Table(
    'links',
    metadata,
    Column('endpoint', String(255)),
    Column('url', String(255))
)


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

        global engine
        engine = await create_engine(
            host='db',
            port=3306,
            user='user',
            password='password',
            db='db',
            loop=loop
        )

        await db_cursor.close()
        conn.close()


@app.route('/api/links', methods=['GET'])
async def get_links(request):
    try:
        loop = get_event_loop()
        global engine
        async with engine.acquire() as conn:
            data = []
            queryset = await conn.execute(table.select())
            for row in await queryset.fetchall():
                data.append({
                    'endpoint': row.endpoint,
                    'url': row.url
                })

            conn.close()
            return json(dumps(data), status=200)

    except Exception as error:
        print(error)
        return json({'message': 'getting links failed'}, status=500)


@app.route('/<link_endpoint>')
async def redirect_link(request, link_endpoint):
    try:
        loop = get_event_loop()
        global engine
        async with engine.acquire() as conn:
            sel = select([table]).where(
                table.columns['endpoint'] == link_endpoint
            )
            query = await conn.execute(sel)
            url = await query.fetchone()

            conn.close()
            return response.redirect(url[1])

    except Exception as error:
        print(error)
        return json({'message': 'link does not exist'}, status=400)


if (__name__ == '__main__'):
    app.run(host='0.0.0.0', port=8000)
