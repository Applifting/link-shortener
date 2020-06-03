'''
Copyright (C) 2020 Link Shortener Authors (see AUTHORS in Documentation).
Licensed under the MIT (Expat) License (see LICENSE in Documentation).
'''
import hashlib

from link_shortener.models import links, salts


async def check_form(request, link_id):
    try:
        async with request.app.engine.acquire() as conn:
            try:
                query = await conn.execute(links.select().where(
                    links.columns['id'] == link_id
                ).where(
                    links.columns['password'] != None
                ))
                link_data = await query.fetchone()
                if not link_data:
                    raise Exception

                return ('password_form.html', link_data, 200)

            except Exception:
                return (
                    'message.html',
                    'Link has no password or does not exist',
                    404
                )

    except Exception:
        return ('message.html', 'Authorization failed', 500)


async def check_password(request, link_id, form):
    try:
        async with request.app.engine.acquire() as conn:
            try:
                link_query = await conn.execute(links.select().where(
                    links.columns['id'] == link_id
                ).where(
                    links.columns['password'] != None
                ))
                link_data = await link_query.fetchone()
                salt_query = await conn.execute(salts.select().where(
                    salts.columns['id'] == link_id
                ))
                salt_data = await salt_query.fetchone()
                if (not link_data) or (not salt_data):
                    raise Exception

                password = hashlib.pbkdf2_hmac(
                    'sha256',
                    form.password.data.encode('utf-8'),
                    salt_data.salt,
                    100000
                )
                if (link_data.password == password):
                    return (link_data.url, None)

                return ('Incorrect password', 401)

            except Exception:
                return ('Link has no password or does not exist', 404)

    except Exception:
        return ('Form failed', 500)
