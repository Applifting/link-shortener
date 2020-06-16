'''
Copyright (C) 2020 Link Shortener Authors (see AUTHORS in Documentation).
Licensed under the MIT (Expat) License (see LICENSE in Documentation).
'''
import os
import hashlib

from link_shortener.models import links, salts

from link_shortener.core.exceptions import NotFoundException


async def check_update_form(request, link_id):
    try:
        async with request.app.engine.acquire() as conn:
            try:
                query = await conn.execute(links.select().where(
                    links.columns['id'] == link_id
                ))
                link_data = await query.fetchone()
                if not link_data:
                    raise Exception

                return ('edit_form.html', link_data, 200)

            except Exception:
                return ('message.html', 'Link does not exist', 404)

    except Exception:
        return ('message.html', 'Authorization failed', 500)


async def update_link(request, link_id, data):
    try:
        async with request.app.engine.acquire() as conn:
            trans = await conn.begin()
            link_update = links.update().where(links.columns['id'] == link_id)
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

            if data['password']:
                salt = os.urandom(32)
                password = hashlib.pbkdf2_hmac(
                    'sha256',
                    data['password'].encode('utf-8'),
                    salt,
                    100000
                )
                if link_data.password:
                    await conn.execute(salts.update().where(
                        salts.columns['link_id'] == link_id
                    ).values(salt=salt))
                else:
                    await conn.execute(salts.insert().values(
                        link_id=link_id,
                        salt=salt
                    ))

                await conn.execute(link_update.values(
                    url=data['url'],
                    switch_date=data['switch_date'],
                    password=password
                ))

            else:
                await conn.execute(link_update.values(
                    url=data['url'],
                    switch_date=data['switch_date']
                ))

            await trans.commit()
            await trans.close()
            return ('Link updated successfully', 200)

    except Exception:
        await trans.close()
        return ('Editing link failed', 500)


async def reset_password(request, link_id):
    async with request.app.engine.acquire() as conn:
        trans = await conn.begin()
        try:
            query = await conn.execute(links.select().where(
                links.columns['id'] == link_id
            ).where(
                links.columns['password'] != None
            ))
            link_data = await query.fetchone()
            await conn.execute(links.update().where(
                links.columns['id'] == link_data.id
            ).values(password=None))
            await conn.execute(salts.delete().where(
                salts.columns['link_id'] == link_data.id
            ))
            await trans.commit()
            await trans.close()

        except AttributeError:
            await trans.close()
            raise NotFoundException
