'''
Copyright (C) 2020 Link Shortener Authors (see AUTHORS in Documentation).
Licensed under the MIT (Expat) License (see LICENSE in Documentation).
'''
from link_shortener.models import links


async def redirect_link(request, link_endpoint):
    try:
        async with request.app.engine.acquire() as conn:
            try:
                query = await conn.execute(links.select().where(
                    links.columns['endpoint'] == link_endpoint
                ).where(
                    links.columns['is_active'] == True
                ))
                link_data = await query.fetchone()
                if not link_data:
                    raise Exception

                if link_data.password:
                    return ('/authorize/{}'.format(link_data.id), None)

                return (link_data.url, None)

            except Exception:
                return ('Link inactive or does not exist', 404)

    except Exception:
        return ('Server error', 500)
