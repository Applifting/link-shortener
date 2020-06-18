'''
Copyright (C) 2020 Link Shortener Authors (see AUTHORS in Documentation).
Licensed under the MIT (Expat) License (see LICENSE in Documentation).
'''
import os
import hashlib

from datetime import date

from link_shortener.models import links, salts

from link_shortener.core.exceptions import (FormInvalidException,
                                            IncorrectDataFormat,
                                            MissingDataException,
                                            NotFoundException)


async def check_update_form(request, link_id):
    async with request.app.engine.acquire() as conn:
        try:
            query = await conn.execute(links.select().where(
                links.columns['id'] == link_id
            ))
            link_data = await query.fetchone()
            if not link_data:
                raise AttributeError

            return link_data

        except AttributeError:
            raise NotFoundException


async def update_link(request, link_id, data, from_api=True):
    # Handle input data
    if from_api:
        try:
            update_data = {
                'password': None,
                'url': data['url'],
                'switch_date': date(
                    data['switch_date']['Year'],
                    data['switch_date']['Month'],
                    data['switch_date']['Day']
                )
            }
        except KeyError:
            raise MissingDataException
        except TypeError:
            raise IncorrectDataFormat

    else:
        if not data.validate():
            raise FormInvalidException

        update_data = {
            'password': data.password.data,
            'url': data.url.data,
            'switch_date': data.switch_date.data
        }

    # Update data in the database
    async with request.app.engine.acquire() as conn:
        trans = await conn.begin()
        link_update = links.update().where(links.columns['id'] == link_id)
        try:
            query = await conn.execute(links.select().where(
                links.columns['id'] == link_id
            ))
            link_data = await query.fetchone()
            if not link_data:
                raise AttributeError

        except AttributeError:
            await trans.close()
            raise NotFoundException

        if update_data['password']:
            salt = os.urandom(32)
            password = hashlib.pbkdf2_hmac(
                'sha256',
                update_data['password'].encode('utf-8'),
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

            await conn.execute(link_update.values(
                url=update_data['url'],
                switch_date=update_data['switch_date'],
                password=password
            ))

        else:
            await conn.execute(link_update.values(
                url=update_data['url'],
                switch_date=update_data['switch_date']
            ))

        await trans.commit()
        await trans.close()


async def reset_password(request, link_id):
    async with request.app.engine.acquire() as conn:
        trans = await conn.begin()
        try:
            query = await conn.execute(links.select().where(
                links.columns['id'] == link_id
            ).where(
                links.columns['password'] != None
            ))
            link_data = await query.fetchone()
            await conn.execute(links.update().where(
                links.columns['id'] == link_data.id
            ).values(password=None))
            await conn.execute(salts.delete().where(
                salts.columns['link_id'] == link_data.id
            ))
            await trans.commit()
            await trans.close()

        except AttributeError:
            await trans.close()
            raise NotFoundException
