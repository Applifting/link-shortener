'''
Copyright (C) 2020 Link Shortener Authors (see AUTHORS in Documentation).
Licensed under the MIT (Expat) License (see LICENSE in Documentation).
'''
from link_shortener.core.exceptions import NotFoundException
from link_shortener.models import links, salts


async def delete_link(request, link_id):
    async with request.app.engine.acquire() as conn:
        trans = await conn.begin()
        try:
            query = await conn.execute(links.select().where(
                links.columns['id'] == link_id
            ))
            link_data = await query.fetchone()
            await conn.execute(links.delete().where(
                links.columns['id'] == link_data.id
            ))
            await conn.execute(salts.delete().where(
                salts.columns['link_id'] == link_data.id
            ))
            await trans.commit()
            await trans.close()

        except AttributeError:
            await trans.close()
            raise NotFoundException
