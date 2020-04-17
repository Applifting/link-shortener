'''
Copyright (C) 2020 Link Shortener Authors (see AUTHORS in Documentation).
Licensed under the MIT (Expat) License (see LICENSE in Documentation).
'''
from sanic import Blueprint

from aiomysql import create_pool
from aiomysql.sa import create_engine

from sqlalchemy import MetaData, Table, Column, String
from sqlalchemy.schema import CreateTable


initdb_blueprint = Blueprint('intitialise_db')

metadata = MetaData()
initdb_blueprint.active_table = Table(
    'active_links',
    metadata,
    Column('owner', String(50)),
    Column('owner_id', String(255)),
    Column('endpoint', String(20), unique=True),
    Column('url', String(300))
)
initdb_blueprint.inactive_table = Table(
    'inactive_links',
    metadata,
    Column('owner', String(50)),
    Column('owner_id', String(255)),
    Column('endpoint', String(20)),
    Column('url', String(300))
)
active_data = [
    (
        'vojtech.janousek@applifting.cz',
        '100793120005790639839',
        'pomuzemesi',
        'https://staging.pomuzeme.si'
    ),
    (
        'vojtech.janousek@applifting.cz',
        '100793120005790639839',
        'vlk',
        'http://www.vlk.cz'
    ),
    (
        'vojtech.janousek@applifting.cz',
        '100793120005790639839',
        'manatee',
        'https://cdn.mos.cms.futurecdn.net/sBVkBoQfStZJWtLwgFRtPi-320-80.jpg'
    ),
    (
        'radek.holy@applifting.cz',
        'unknown',
        'dollar',
        'https://i.kym-cdn.com/entries/icons/facebook/000/013/285/gangsta-animals.jpg'
    ),
    (
        'radek.holy@applifting.cz',
        'unknown',
        'kodex',
        'https://github.com/Applifting/culture'
    ),
    (
        'radek.holy@applifting.cz',
        'unknown',
        'meta',
        'https://github.com/Applifting/link-shortener'
    )
]
inactive_data = [
    (
        'vojtech.janousek@applifting.cz',
        '100793120005790639839',
        'tunak',
        'https://www.britannica.com/animal/tuna-fish'
    ),
    (
        'radek.holy@applifting.cz',
        'unknown',
        'nope',
        'https://www.youtube.com/watch?v=gvdf5n-zI14'
    )
]

@initdb_blueprint.listener('before_server_start')
async def initialise_db(app, loop):
    pool = await create_pool(
        host='db',
        port=3306,
        user='user',
        password='password',
        db='db',
        loop=loop,
        autocommit=True
    )
    app.engine = await create_engine(
        host='db',
        port=3306,
        user='user',
        password='password',
        db='db',
        loop=loop
    )
    async with pool.acquire() as conn:
        db_cursor = await conn.cursor()
        try:
            await db_cursor.execute(
                str(CreateTable(initdb_blueprint.active_table))
            )
            await db_cursor.execute(
                str(CreateTable(initdb_blueprint.inactive_table))
            )
            await db_cursor.executemany(
                'INSERT INTO active_links (owner, owner_id, endpoint, url) \
                 VALUES (%s, %s, %s, %s)',
                active_data
            )
            await db_cursor.executemany(
                'INSERT INTO inactive_links (owner, owner_id, endpoint, url) \
                 VALUES (%s, %s, %s, %s)',
                inactive_data
            )

        except Exception as error:
            print(str(error) + '\n' + 'Tables are probably already cached')

        await db_cursor.close()

    pool.terminate()
    await pool.wait_closed()


@initdb_blueprint.listener('after_server_stop')
async def close_engine(app, loop):
    app.engine.terminate()
    await app.engine.wait_closed()
