'''
Copyright (C) 2020 Link Shortener Authors (see AUTHORS in Documentation).
Licensed under the MIT (Expat) License (see LICENSE in Documentation).
'''
import os
import hashlib

from link_shortener.models import links, salts

from link_shortener.core.exceptions import DuplicateActiveLinkForbidden


async def create_link(request, data):
    async with request.app.engine.acquire() as conn:
        trans = await conn.begin()
        try:
            query = await conn.execute(links.select().where(
                links.columns['endpoint'] == data['endpoint']
            ).where(
                links.columns['is_active'] == True
            ))
            link_data = await query.fetchone()
            if link_data:
                await trans.close()
                raise DuplicateActiveLinkForbidden

        except AttributeError:
            await trans.close()
            raise DuplicateActiveLinkForbidden

        if data['password']:
            salt = os.urandom(32)
            password = hashlib.pbkdf2_hmac(
                'sha256',
                data['password'].encode('utf-8'),
                salt,
                100000)
        else:
            password = None

        link_object = await conn.execute(links.insert().values(
            owner=data['owner'],
            owner_id=data['owner_id'],
            password=password,
            endpoint=data['endpoint'],
            url=data['url'],
            switch_date=data['switch_date'],
            is_active=True
        ))
        if password:
            await conn.execute(salts.insert().values(
                link_id=link_object.lastrowid,
                salt=salt
            ))

        await trans.commit()
        await trans.close()
