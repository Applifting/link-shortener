'''
Copyright (C) 2020 Link Shortener Authors (see AUTHORS in Documentation).
Licensed under the MIT (Expat) License (see LICENSE in Documentation).
'''
import os
import hashlib

from link_shortener.models import links, salts

from link_shortener.core.exceptions import NotFoundException


async def check_update_form(request, link_id):
    async with request.app.engine.acquire() as conn:
        query = await conn.execute(links.select().where(
            links.columns['id'] == link_id
        ))
        link_data = await query.fetchone()
        if not link_data:
            raise NotFoundException

        return link_data


async def update_link(request, link_id, data):
    async with request.app.engine.acquire() as conn:
        trans = await conn.begin()
        link_update = links.update().where(links.columns['id'] == link_id)
        query = await conn.execute(links.select().where(
            links.columns['id'] == link_id
        ))
        link_data = await query.fetchone()
        if not link_data:
            await trans.close()
            raise NotFoundException

        if data['password'] != 20 * '\u25CF':
                if data['password']:
                    salt = os.urandom(32)
                    password = hashlib.pbkdf2_hmac(
                        'sha256',
                        data['password'].encode('utf-8'),
                        salt,
                        100000
                    )
                    if link_data.password:
                        await conn.execute(salts.update().where(
                            salts.columns['link_id'] == link_id
                        ).values(salt=salt))
                    else:
                        await conn.execute(salts.insert().values(
                            link_id=link_id,
                            salt=salt
                        ))
                else:
                    password = None

                await conn.execute(link_update.values(
                    url=data['url'],
                    switch_date=data['switch_date'],
                    password=password
                ))

        else:
            await conn.execute(link_update.values(
                url=data['url'],
                switch_date=data['switch_date']
            ))

        await trans.commit()
        await trans.close()


async def reset_password(request, link_id):
    async with request.app.engine.acquire() as conn:
        trans = await conn.begin()
        query = await conn.execute(links.select().where(
            links.columns['id'] == link_id
        ).where(
            links.columns['password'] != None
        ))
        link_data = await query.fetchone()
        if not link_data:
            await trans.close()
            raise NotFoundException

        await conn.execute(links.update().where(
            links.columns['id'] == link_data.id
        ).values(password=None))
        await conn.execute(salts.delete().where(
            salts.columns['link_id'] == link_data.id
        ))
        await trans.commit()
        await trans.close()
