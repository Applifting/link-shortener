'''
Copyright (C) 2020 Link Shortener Authors (see AUTHORS in Documentation).
Licensed under the MIT (Expat) License (see LICENSE in Documentation).
'''
import hashlib
import os

from aiopg.sa import create_engine
from decouple import config
from sanic import Blueprint

from link_shortener.core.test_data import data
from link_shortener.models import links, salts

initdb_blueprint = Blueprint('intitialise_db')

engine_data = f"postgresql://" \
              f"{config('POSTGRES_USER')}:" \
              f"{config('POSTGRES_PASSWORD')}@" \
              f"{config('POSTGRES_HOST')}:" \
              f"{config('POSTGRES_PORT')}/" \
              f"{config('POSTGRES_DB')}?sslmode=preferred" \
    if config('PRODUCTION', default=False, cast=bool) \
    else 'postgresql://postgres:postgres@db:5432/db'


@initdb_blueprint.listener('before_server_start')
async def initialise_db(app, loop):
    app.engine = await create_engine(engine_data)
    async with app.engine.acquire() as conn:
        try:
            trans = await conn.begin()
            if not config('PRODUCTION', default=False, cast=bool):
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
                        link = await link_object.fetchone()
                        await conn.execute(salts.insert().values(
                            link_id=link.id,
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
            print(str(error))


@initdb_blueprint.listener('after_server_stop')
async def close_engine(app, loop):
    app.engine.terminate()
    await app.engine.wait_closed()
