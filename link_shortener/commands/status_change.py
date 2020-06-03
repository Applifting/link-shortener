'''
Copyright (C) 2020 Link Shortener Authors (see AUTHORS in Documentation).
Licensed under the MIT (Expat) License (see LICENSE in Documentation).
'''
from link_shortener.models import links


async def activate_link(request, link_id):
    try:
        async with request.app.engine.acquire() as conn:
            trans = await conn.begin()
            try:
                query = await conn.execute(links.select().where(
                    links.columns['id'] == link_id
                ))
                link_data = await query.fetchone()
                if not link_data:
                    raise Exception

            except Exception:
                await trans.close()
                return ('Link does not exist', 404)

            try:
                endpoint_query = await conn.execute(links.select().where(
                    links.columns['endpoint'] == link_data.endpoint
                ).where(
                    links.columns['is_active'] == True
                ).where(
                    links.columns['id'] != link_id
                ))
                active_endpoint = await endpoint_query.fetchone()
                if not active_endpoint:
                    raise Exception

                await trans.close()
                return (
                    'An active endpoint with that name already exists',
                    400
                )

            except Exception:
                await conn.execute(links.update().where(
                    links.columns['id'] == link_id
                ).values(is_active=True))
                await trans.commit()
                await trans.close()
                return ('Link activated successfully', 200)

    except Exception:
        await trans.close()
        return ('Activating link failed', 500)
