'''
Copyright (C) 2020 Link Shortener Authors (see AUTHORS in Documentation).
Licensed under the MIT (Expat) License (see LICENSE in Documentation).
'''
from link_shortener.models import links, salts


async def delete_link(request, link_id):
    try:
        async with request.app.engine.acquire() as conn:
            trans = await conn.begin()
            query = await conn.execute(
                links.select().where(
                    links.columns['id'] == link_id
                )
            )
            try:
                link_data = await query.fetchone()
                if not link_data:
                    raise Exception

                await conn.execute(links.delete().where(
                    links.columns['id'] == link_data.id
                ))
                await conn.execute(salts.delete().where(
                    salts.columns['id'] == link_data.id
                ))
                await trans.commit()
                await trans.close()
                return ('Link successfully deleted', 200)

            except Exception:
                await trans.close()
                return ('Link does not exist', 404)

    except Exception:
        await trans.close()
        return ('Deleting link failed', 500)
