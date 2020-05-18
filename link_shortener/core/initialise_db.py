'''
Copyright (C) 2020 Link Shortener Authors (see AUTHORS in Documentation).
Licensed under the MIT (Expat) License (see LICENSE in Documentation).
'''
import os
import uuid
import hashlib
import datetime

from decouple import config

from sanic import Blueprint

from aiomysql.sa import create_engine

from sqlalchemy.schema import CreateTable

from link_shortener.models import actives, inactives, salts


initdb_blueprint = Blueprint('intitialise_db')


active_data = [
    [
        str(uuid.uuid1()),
        'vojtech.janousek@applifting.cz',
        '100793120005790639839',
        None,
        'pomuzemesi',
        'https://staging.pomuzeme.si',
        None
    ],
    [
        str(uuid.uuid1()),
        'vojtech.janousek@applifting.cz',
        '100793120005790639839',
        None,
        'vlk',
        'http://www.vlk.cz',
        datetime.date(2020, 5, 6)
    ],
    [
        str(uuid.uuid1()),
        'vojtech.janousek@applifting.cz',
        '100793120005790639839',
        'bigfish',
        'manatee',
        'https://cdn.mos.cms.futurecdn.net/sBVkBoQfStZJWtLwgFRtPi-320-80.jpg',
        None
    ],
    [
        str(uuid.uuid1()),
        'radek.holy@applifting.cz',
        'unknown',
        None,
        'dollar',
        'https://splittingmytime.com/wp-content/uploads/2019/03/bfd.jpg',
        datetime.date(2020, 5, 8)
    ],
    [
        str(uuid.uuid1()),
        'radek.holy@applifting.cz',
        'unknown',
        None,
        'kodex',
        'https://github.com/Applifting/culture',
        None
    ],
    [
        str(uuid.uuid1()),
        'radek.holy@applifting.cz',
        'unknown',
        'metapass',
        'meta',
        'https://github.com/Applifting/link-shortener',
        None
    ]
]
inactive_data = [
    [
        str(uuid.uuid1()),
        'vojtech.janousek@applifting.cz',
        '100793120005790639839',
        'tunak',
        'https://www.britannica.com/animal/tuna-fish',
        datetime.date(2020, 6, 1)
    ],
    [
        str(uuid.uuid1()),
        'radek.holy@applifting.cz',
        'unknown',
        'nope',
        'https://www.youtube.com/watch?v=gvdf5n-zI14',
        None
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
        app.engine = await create_engine(
            host='db',
            port=3306,
            user='user',
            password='password',
            db='db',
            loop=loop
        )
    async with app.engine.acquire() as conn:
        try:
            trans = await conn.begin()

            await conn.execute(CreateTable(actives))
            await conn.execute(CreateTable(inactives))
            await conn.execute(CreateTable(salts))
            for values in active_data:
                if values[3] is not None:
                    salt = os.urandom(32)
                    values[3] = hashlib.pbkdf2_hmac(
                        'sha256',
                        values[3].encode('utf-8'),
                        salt,
                        100000
                    )
                    await conn.execute(
                        salts.insert().values(
                            identifier=values[0],
                            salt=salt
                        )
                    )

                await conn.execute(
                    actives.insert().values(
                        identifier=values[0],
                        owner=values[1],
                        owner_id=values[2],
                        password=values[3],
                        endpoint=values[4],
                        url=values[5],
                        switch_date=values[6]
                    )
                )
            for values in inactive_data:
                await conn.execute(
                    inactives.insert().values(
                        identifier=values[0],
                        owner=values[1],
                        owner_id=values[2],
                        endpoint=values[3],
                        url=values[4],
                        switch_date=values[5]
                    )
                )
            await trans.commit()
            await trans.close()

        except Exception as error:
            await trans.close()
            print(str(error) + '\n' + 'Tables are already cached')


@initdb_blueprint.listener('after_server_stop')
async def close_engine(app, loop):
    app.engine.terminate()
    await app.engine.wait_closed()
