'''
Copyright (C) 2020 Link Shortener Authors (see AUTHORS in Documentation).
Licensed under the MIT (Expat) License (see LICENSE in Documentation).
'''
from datetime import date
from decouple import config
from json import loads

from sanic import Blueprint
from sanic.response import json

from sqlalchemy.sql.expression import select as sql_select

from link_shortener.models import actives, inactives


api_switcher_blueprint = Blueprint('switchers')


@api_switcher_blueprint.route('/api/status/activate', methods=['POST'])
async def activate_due_links(request):
    try:
        token = request.headers['Bearer']
        if (token != config('ACCESS_TOKEN')):
            return json({'message': 'Unauthorized'}, status=401)

    except KeyError:
        return json({'message': 'Please provide a token'}, status=400)

    try:
        data = request.body.decode().split('&')
        year = int(data[0][5:])
        month = int(data[1][6:])
        day = int(data[2][4:])

        switch_date = date(year, month, day)

    except KeyError:
        return json({'message': 'Please provide the date'}, status=400)

    except Exception:
        return json({'message': 'Incorrect payload'}, status=400)

    try:
        async with request.app.engine.acquire() as conn:
            trans = await conn.begin()
            queryset = await conn.execute(
                inactives.select().where(
                    inactives.columns['switch_date'] == switch_date
                )
            )
            link_data = await queryset.fetchall()
            if not link_data:
                await trans.close()
                return json({'message': 'No links to activate'}, status=200)

            count = 0
            for link in link_data:
                count += 1
                await conn.execute(
                    actives.insert().from_select(
                        [
                            'identifier',
                            'owner',
                            'owner_id',
                            'password',
                            'endpoint',
                            'url'
                        ],
                        sql_select([
                            inactives.c.identifier,
                            inactives.c.owner,
                            inactives.c.owner_id,
                            inactives.c.password,
                            inactives.c.endpoint,
                            inactives.c.url
                        ]).where(inactives.c.id == link.id)
                    )
                )
                await conn.execute(
                    inactives.delete().where(
                        inactives.columns['id'] == link.id
                    )
                )

            await trans.commit()
            await trans.close()
            return json(
                {'message': '{} links successfully activated'.format(count)},
                status=200
            )

    except Exception:
        await trans.close()
        return json({'message': 'Activating links failed'}, status=500)


@api_switcher_blueprint.route('/api/status/deactivate', methods=['POST'])
async def deactivate_due_links(request):
    try:
        token = request.headers['Bearer']
        if (token != config('ACCESS_TOKEN')):
            return json({'message': 'Unauthorized'}, status=401)

    except KeyError:
        return json({'message': 'Please provide a token'}, status=400)

    try:
        data = request.body.decode().split('&')
        year = int(data[0][5:])
        month = int(data[1][6:])
        day = int(data[2][4:])

        switch_date = date(year, month, day)

    except KeyError:
        return json({'message': 'Please provide the date'}, status=400)

    except Exception:
        return json({'message': 'Incorrect payload'}, status=400)

    try:
        async with request.app.engine.acquire() as conn:
            trans = await conn.begin()
            queryset = await conn.execute(
                actives.select().where(
                    actives.columns['switch_date'] == switch_date
                )
            )
            link_data = await queryset.fetchall()
            if not link_data:
                await trans.close()
                return json({'message': 'No links to deactivate'}, status=200)

            count = 0
            for link in link_data:
                count += 1
                await conn.execute(
                    inactives.insert().from_select(
                        [
                            'identifier',
                            'owner',
                            'owner_id',
                            'password',
                            'endpoint',
                            'url'
                        ],
                        sql_select([
                            actives.c.identifier,
                            actives.c.owner,
                            actives.c.owner_id,
                            actives.c.password,
                            actives.c.endpoint,
                            actives.c.url
                        ]).where(actives.c.id == link.id)
                    )
                )
                await conn.execute(
                    actives.delete().where(
                        actives.columns['id'] == link.id
                    )
                )

            await trans.commit()
            await trans.close()
            return json(
                {'message': '{} links successfully deactivated'.format(count)},
                status=200
            )

    except Exception:
        await trans.close()
        return json({'message': 'Deactivating links failed'}, status=500)
