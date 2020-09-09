'''
Copyright (C) 2020 Link Shortener Authors (see AUTHORS in Documentation).
Licensed under the MIT (Expat) License (see LICENSE in Documentation).
'''
from sqlalchemy import and_

from link_shortener.core.exceptions import NotFoundException
from link_shortener.models import links


async def redirect_link(request, link_endpoint):
    async with request.app.engine.acquire() as conn:
        try:
            query = await conn.execute(links.select().where(
                and_(
                    links.columns['endpoint'] == link_endpoint,
                    links.columns['is_active'] == True
                )))
            link_data = await query.fetchone()
            if link_data.password is not None:
                return '/authorize/{}'.format(link_data.id)

            return link_data.url

        except AttributeError:
            raise NotFoundException
