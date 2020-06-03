'''
Copyright (C) 2020 Link Shortener Authors (see AUTHORS in Documentation).
Licensed under the MIT (Expat) License (see LICENSE in Documentation).
'''
from link_shortener.models import links, salts


async def reset_password(request, link_id):
    try:
        async with request.app.engine.acquire() as conn:
            trans = await conn.begin()
            try:
                query = await conn.execute(links.select().where(
                    links.columns['id'] == link_id
                ).where(
                    links.columns['password'] != None
                ))
                link_data = await query.fetchone()
                if not link_data:
                    raise Exception

                await conn.execute(links.update().where(
                    links.columns['id'] == link_id
                ).values(password=None))
                await conn.execute(salts.delete().where(
                    salts.columns['id'] == link_id
                ))
                await trans.commit()
                await trans.close()
                return ('Password reset successfully', 200)

            except Exception:
                await trans.close()
                return ('Link has no password or does not exist', 404)

    except Exception:
        await trans.close()
        return ('Resetting password failed', 500)
