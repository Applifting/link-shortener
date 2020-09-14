'''
Copyright (C) 2020 Link Shortener Authors (see AUTHORS in Documentation).
Licensed under the MIT (Expat) License (see LICENSE in Documentation).
'''
import hashlib

from sqlalchemy import and_
from decouple import config

from link_shortener.models import links, salts
from link_shortener.core.exceptions import (AccessDeniedException,
                                            FormInvalidException,
                                            NotFoundException)


async def check_auth_form(request, link_id):
    async with request.app.engine.acquire() as conn:
        query = await conn.execute(links.select().where(
            and_(
            links.columns['id'] == link_id,
            links.columns['password'] != None
        )))
        link_data = await query.fetchone()
        if not link_data:
            raise NotFoundException

        return link_data


async def check_password(request, link_id, form):
    if not form.validate():
        raise FormInvalidException

    async with request.app.engine.acquire() as conn:
        try:
            link_query = await conn.execute(links.select().where(
                and_(
                links.columns['id'] == link_id,
                links.columns['password'] != None
            )))
            link_data = await link_query.fetchone()
            salt_query = await conn.execute(salts.select().where(
                salts.columns['link_id'] == link_data.id
            ))
            salt_data = await salt_query.fetchone()

            password = hashlib.pbkdf2_hmac(
                'sha256',
                form.password.data.encode('utf-8'),
                salt_data.salt,
                100000
            )
            if (link_data.password != password):
                raise AccessDeniedException

            return link_data.url

        except AttributeError as error:
            print(error)
            raise NotFoundException


async def check_token(request):
    try:
        token = request.headers['Bearer']
        if (token != config('ACCESS_TOKEN')):
            raise AccessDeniedException

    except KeyError:
        raise AccessDeniedException
