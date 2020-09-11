'''
Copyright (C) 2020 Link Shortener Authors (see AUTHORS in Documentation).
Licensed under the MIT (Expat) License (see LICENSE in Documentation).
'''
import os
import hashlib
import datetime

from decouple import config

from sanic import Blueprint

#from aiomysql.sa import create_engine
from aiopg.sa import create_engine


from sqlalchemy.schema import CreateTable

from link_shortener.models import links, salts


initdb_blueprint = Blueprint('intitialise_db')


data = [
    [
        'vojtech.janousek@applifting.cz',
        '100793120005790639839',
        'yolo',
        'pomuzemesi',
        'https://staging.pomuzeme.si',
        None,
        True
    ],
    [
        'vojtech.janousek@applifting.cz',
        '100793120005790639839',
        None,
        'vlk',
        'http://www.vlk.cz',
        datetime.date(2020, 5, 6),
        True
    ],
    [
        'vojtech.janousek@applifting.cz',
        '100793120005790639839',
        None,
        'manatee',
        'https://cdn.mos.cms.futurecdn.net/sBVkBoQfStZJWtLwgFRtPi-320-80.jpg',
        None,
        True
    ],
    [
        'radek.holy@applifting.cz',
        'unknown',
        None,
        'dollar',
        'https://splittingmytime.com/wp-content/uploads/2019/03/bfd.jpg',
        datetime.date(2020, 5, 8),
        True
    ],
    [
        'radek.holy@applifting.cz',
        'unknown',
        'dsadsa',
        'kodex',
        'https://github.com/Applifting/culture',
        None,
        True
    ],
    [
        'radek.holy@applifting.cz',
        'unknown',
        None,
        'meta',
        'https://github.com/Applifting/link-shortener',
        None,
        True
    ],
    [
        'vojtech.janousek@applifting.cz',
        '100793120005790639839',
        'dasdsa',
        'tunak',
        'https://www.britannica.com/animal/tuna-fish',
        datetime.date(2020, 6, 1),
        False
    ],
    [
        'radek.holy@applifting.cz',
        'unknown',
        None,
        'nope',
        'https://www.youtube.com/watch?v=gvdf5n-zI14',
        None,
        False
    ],
    [
        'vojtech.janousek@applifting.cz',
        '100793120005790639839',
        None,
        'vlk',
        'https://google.com',
        None,
        False
    ],
    [
        'vojtech.janousek@applifting.cz',
        '100793120005790639839',
        None,
        'anothertunak',
        'https://www.britannica.com/animal/tuna-fish',
        datetime.date(2020, 6, 1),
        True
    ]
]


@initdb_blueprint.listener('before_server_start')
async def initialise_db(app, loop):
    if config('PRODUCTION', default=False, cast=bool):
        app.engine = await create_engine(
            host=config('MYSQL_HOST'),
            port=config('MYSQL_PORT', cast=int),
            user=config('MYSQL_USER'),
            password=config('MYSQL_PASSWORD'),
            db=config('MYSQL_DB'),
            loop=loop
        )
    else:
        #app.engine = create_engine("postgresql+psycopg2://postgres:postgres@localhost:5432/db")
        app.engine = await create_engine(
            host='localhost',
            port=5432,
            user='postgres',
            password='postgres',
            database='db',
            loop=loop,
        )
    async with app.engine.acquire() as conn:
        try:
            trans = await conn.begin()
            await conn.execute(CreateTable(links))
            await conn.execute(CreateTable(salts))
            for values in data:
                if values[2]:
                    salt = os.urandom(32)
                    values[2] = hashlib.pbkdf2_hmac(
                        'sha256',
                        values[2].encode('utf-8'),
                        salt,
                        100000
                    )
                    link_object = await conn.execute(links.insert().values(
                        owner=values[0],
                        owner_id=values[1],
                        password=values[2],
                        endpoint=values[3],
                        url=values[4],
                        switch_date=values[5],
                        is_active=values[6]
                    ))

                    link_id = await link_object.fetchone()
                    link_id = link_id[0]
                    await conn.execute(salts.insert().values(
                        link_id=link_id,
                        salt=salt
                    ))
                else:
                    await conn.execute(links.insert().values(
                        owner=values[0],
                        owner_id=values[1],
                        password=values[2],
                        endpoint=values[3],
                        url=values[4],
                        switch_date=values[5],
                        is_active=values[6]
                    ))

            await trans.commit()
            await trans.close()

        except Exception as error:
            await trans.close()
            print(str(error) + '\n' + 'Tables are already cached')


@initdb_blueprint.listener('after_server_stop')
async def close_engine(app, loop):
    app.engine.terminate()
    await app.engine.wait_closed()
