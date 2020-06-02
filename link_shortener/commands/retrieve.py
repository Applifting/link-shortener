'''
Copyright (C) 2020 Link Shortener Authors (see AUTHORS in Documentation).
Licensed under the MIT (Expat) License (see LICENSE in Documentation).
'''
from decouple import config

from sanic.response import json

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
