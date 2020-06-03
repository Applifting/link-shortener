'''
Copyright (C) 2020 Link Shortener Authors (see AUTHORS in Documentation).
Licensed under the MIT (Expat) License (see LICENSE in Documentation).
'''
from link_shortener.models import links, salts


async def check_password_form(request, link_id):
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
