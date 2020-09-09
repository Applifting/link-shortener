'''
Copyright (C) 2020 Link Shortener Authors (see AUTHORS in Documentation).
Licensed under the MIT (Expat) License (see LICENSE in Documentation).
'''
from sqlalchemy import and_

from link_shortener.models import links

from link_shortener.core.exceptions import (DuplicateActiveLinkForbidden,
                                            NotFoundException)


async def activate_link(request, link_id):
    async with request.app.engine.acquire() as conn:
        trans = await conn.begin()
        try:
            query = await conn.execute(links.select().where(
                links.columns['id'] == link_id
            ))
            link_data = await query.fetchone()

            endpoint_query = await conn.execute(links.select().where(
                and_(
                links.columns['endpoint'] == link_data.endpoint,
                links.columns['id'] != link_id
            )))
            for link in await endpoint_query.fetchall():
                if link.is_active:
                    await trans.close()
                    raise DuplicateActiveLinkForbidden

            await conn.execute(links.update().where(
                links.columns['id'] == link_id
            ).values(is_active=True))
            await trans.commit()
            await trans.close()

        except AttributeError:
            await trans.close()
            raise NotFoundException


async def deactivate_link(request, link_id):
    async with request.app.engine.acquire() as conn:
        trans = await conn.begin()
        try:
            query = await conn.execute(links.select().where(
                links.columns['id'] == link_id
            ))
            link_data = await query.fetchone()

            await conn.execute(links.update().where(
                links.columns['id'] == link_data.id
            ).values(is_active=False))
            await trans.commit()
            await trans.close()

        except AttributeError:
            await trans.close()
            raise NotFoundException
