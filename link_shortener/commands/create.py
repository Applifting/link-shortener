'''
Copyright (C) 2020 Link Shortener Authors (see AUTHORS in Documentation).
Licensed under the MIT (Expat) License (see LICENSE in Documentation).
'''
import hashlib
import os

from link_shortener.commands.validation import (endpoint_duplicity_check,
                                                url_validation)
from link_shortener.models import links, salts


async def create_link(request, data):
    async with request.app.engine.acquire() as conn:
        await endpoint_duplicity_check(conn, data)

        trans = await conn.begin()

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
            url=await url_validation(data['url'], trans),
            switch_date=data['switch_date'],
            is_active=True
        ))
        if password:
            link = await link_object.fetchone()
            await conn.execute(salts.insert().values(
                link_id=link.id,
                salt=salt
            ))

        await trans.commit()
        await trans.close()
