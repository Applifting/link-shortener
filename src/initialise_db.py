'''
Copyright (C) 2020 Link Shortener Authors (see AUTHORS in Documentation).
Licensed under the MIT (Expat) License (see LICENSE in Documentation).
'''
import uuid

from sanic import Blueprint

from aiomysql.sa import create_engine

from sqlalchemy.schema import CreateTable

from models import actives, inactives


initdb_blueprint = Blueprint('intitialise_db')


active_data = [
    (
        str(uuid.uuid1())[:36],
        'vojtech.janousek@applifting.cz',
        '100793120005790639839',
        'pomuzemesi',
        'https://staging.pomuzeme.si'
    ),
    (
        str(uuid.uuid1())[:36],
        'vojtech.janousek@applifting.cz',
        '100793120005790639839',
        'vlk',
        'http://www.vlk.cz'
    ),
    (
        str(uuid.uuid1())[:36],
        'vojtech.janousek@applifting.cz',
        '100793120005790639839',
        'manatee',
        'https://cdn.mos.cms.futurecdn.net/sBVkBoQfStZJWtLwgFRtPi-320-80.jpg'
    ),
    (
        str(uuid.uuid1())[:36],
        'radek.holy@applifting.cz',
        'unknown',
        'dollar',
        'https://splittingmytime.com/wp-content/uploads/2019/03/bfd.jpg'
    ),
    (
        str(uuid.uuid1())[:36],
        'radek.holy@applifting.cz',
        'unknown',
        'kodex',
        'https://github.com/Applifting/culture'
    ),
    (
        str(uuid.uuid1())[:36],
        'radek.holy@applifting.cz',
        'unknown',
        'meta',
        'https://github.com/Applifting/link-shortener'
    )
]
inactive_data = [
    (
        str(uuid.uuid1())[:36],
        'vojtech.janousek@applifting.cz',
        '100793120005790639839',
        'tunak',
        'https://www.britannica.com/animal/tuna-fish'
    ),
    (
        str(uuid.uuid1())[:36],
        'radek.holy@applifting.cz',
        'unknown',
        'nope',
        'https://www.youtube.com/watch?v=gvdf5n-zI14'
    )
]


@initdb_blueprint.listener('before_server_start')
async def initialise_db(app, loop):
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

            await conn.execute(str(CreateTable(actives).compile(app.engine)))
            await conn.execute(str(CreateTable(inactives).compile(app.engine)))
            for values in active_data:
                await conn.execute(
                    actives.insert().values(
                        identifier=values[0],
                        owner=values[1],
                        owner_id=values[2],
                        endpoint=values[3],
                        url=values[4]
                    )
                )
            for values in inactive_data:
                await conn.execute(
                    inactives.insert().values(
                        identifier=values[0],
                        owner=values[1],
                        owner_id=values[2],
                        endpoint=values[3],
                        url=values[4]
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
