'''
Copyright (C) 2020 Link Shortener Authors (see AUTHORS in Documentation).
Licensed under the MIT (Expat) License (see LICENSE in Documentation).
'''
import os
import hashlib

from datetime import date

from link_shortener.models import links, salts

from link_shortener.core.exceptions import (DuplicateActiveLinkForbidden,
                                            FormInvalidException,
                                            IncorrectDataFormat,
                                            MissingDataException)


async def create_link(request, data, user_data=None, from_api=True):
    # Handle input data
    if from_api:
        try:
            link_data = {
                'owner': data['owner'],
                'owner_id': data['owner_id'],
                'password': None,
                'endpoint': data['endpoint'],
                'url': data['url']
            }
            if not isinstance(data['endpoint'], str):
                raise TypeError

            if data['switch_date'] is not None:
                link_data['switch_date'] = date(
                    data['switch_date']['Year'],
                    data['switch_date']['Month'],
                    data['switch_date']['Day']
                )
            else:
                link_data['switch_date'] = None
        except KeyError:
            raise MissingDataException
        except TypeError:
            raise IncorrectDataFormat

    else:
        if not data.validate():
            raise FormInvalidException

        link_data = {
            'owner': user_data.email,
            'owner_id': user_data.id,
            'password': data.password.data,
            'endpoint': data.endpoint.data,
            'url': data.url.data,
            'switch_date': data.switch_date.data
        }

    # Insert data into database
    async with request.app.engine.acquire() as conn:
        trans = await conn.begin()
        query = await conn.execute(links.select().where(
            links.columns['endpoint'] == link_data['endpoint']
        ).where(
            links.columns['is_active'] == True
        ))
        if await query.fetchone():
            await trans.close()
            raise DuplicateActiveLinkForbidden

        if link_data['password']:
            salt = os.urandom(32)
            password = hashlib.pbkdf2_hmac(
                'sha256',
                link_data['password'].encode('utf-8'),
                salt,
                100000
            )
        else:
            password = None

        link_object = await conn.execute(links.insert().values(
            owner=link_data['owner'],
            owner_id=link_data['owner_id'],
            password=password,
            endpoint=link_data['endpoint'],
            url=link_data['url'],
            switch_date=link_data['switch_date'],
            is_active=True
        ))
        if password:
            await conn.execute(salts.insert().values(
                link_id=link_object.lastrowid,
                salt=salt
            ))

        await trans.commit()
        await trans.close()
