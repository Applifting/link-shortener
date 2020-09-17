'''
Copyright (C) 2020 Link Shortener Authors (see AUTHORS in Documentation).
Licensed under the MIT (Expat) License (see LICENSE in Documentation).
'''
from sqlalchemy import and_

from link_shortener.core.exceptions import DuplicateActiveLinkForbidden
from link_shortener.models import links


async def endpoint_duplicity_check(conn, trans, data):
    query = await conn.execute(links.select().where(and_(
        links.columns['endpoint'] == data['endpoint'],
        links.columns['is_active'].is_(True)
    )))
    link_data = await query.fetchone()
    if link_data:
        await trans.close()
        raise DuplicateActiveLinkForbidden
