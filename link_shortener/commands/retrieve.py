'''
Copyright (C) 2020 Link Shortener Authors (see AUTHORS in Documentation).
Licensed under the MIT (Expat) License (see LICENSE in Documentation).
'''
from link_shortener.models import links


async def retrieve_links(request, filters):
    async with request.app.engine.acquire() as conn:
        link_select = links.select()
        for filter in filters.items():
            link_select = link_select.where(
                links.columns[filter[0]] == filter[1]
            )
        queryset = await conn.execute(link_select)
        link_data = await queryset.fetchall()
        return link_data


async def retrieve_link(request, link_id):
    async with request.app.engine.acquire() as conn:
        try:
            query = await conn.execute(links.select().where(
                links.columns['id'] == link_id
            ))
            link_data = await query.fetchone()
            if not link_data:
                raise Exception

            return (link_data, None)

        except Exception:
            return ('Link does not exist', 404)
