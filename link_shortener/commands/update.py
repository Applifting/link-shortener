'''
Copyright (C) 2020 Link Shortener Authors (see AUTHORS in Documentation).
Licensed under the MIT (Expat) License (see LICENSE in Documentation).
'''
import hashlib
import os

from decouple import config
from sqlalchemy import and_

from link_shortener.core.exceptions import NotFoundException
from link_shortener.commands.validation import endpoint_duplicity_check
from link_shortener.models import links, salts


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
        query = await conn.execute(links.select().where(
            links.columns['id'] == link_id
        ))
        link_data = await query.fetchone()

        if not link_data:
            raise NotFoundException

        # Only check for duplicity if the endpoint has changed
        new_endpoint, old_endpoint = data['endpoint'], link_data['endpoint']
        if new_endpoint and (new_endpoint != old_endpoint):
            await endpoint_duplicity_check(conn, data)

        trans = await conn.begin()

        link_update = links.update().where(links.columns['id'] == link_id)

        if data['password'] == config('DEFAULT_PASSWORD'):
            await conn.execute(link_update.values(
                endpoint=data['endpoint'] if data['endpoint'] else link_data['endpoint'],
                url=data['url'] if data['url'] else link_data['url'],
                switch_date=data['switch_date']
            ))
        else:
            if link_data.password:
                await conn.execute(salts.delete().where(
                    salts.columns['link_id'] == link_data.id
                ))

            if not data['password']:
                password = None

            else:
                salt = os.urandom(32)
                password = hashlib.pbkdf2_hmac(
                    'sha256',
                    data['password'].encode('utf-8'),
                    salt,
                    100000
                )
                await conn.execute(salts.insert().values(
                    link_id=link_id,
                    salt=salt
                ))

            await conn.execute(link_update.values(
                endpoint=data['endpoint'] if data['endpoint'] else link_data['endpoint'],
                url=data['url'] if data['url'] else link_data['url'],
                switch_date=data['switch_date'],
                password=password
            ))

        await trans.commit()
        await trans.close()


async def reset_password(request, link_id):
    async with request.app.engine.acquire() as conn:
        trans = await conn.begin()
        query = await conn.execute(links.select().where(and_(
            links.columns['id'] == link_id,
            links.columns['password'].isnot(None)
        )))
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
