'''
Copyright (C) 2020 Link Shortener Authors (see AUTHORS in Documentation).
Licensed under the MIT (Expat) License (see LICENSE in Documentation).
'''
from json import loads
from decouple import config

from sanic import Blueprint
from sanic.response import json

from link_shortener.models import actives, inactives


api_update_link_blueprint = Blueprint('update_link')


@api_update_link_blueprint.route(
    '/api/link/<status>/<link_id>',
    methods=['PUT']
)
async def api_update_link_by_id(request, status, link_id):
    try:
        token = request.headers['Bearer']
        if (token != config('ACCESS_TOKEN')):
            return json({'message': 'Unauthorized'}, status=401)

    except KeyError:
        return json({'message': 'Please provide a token'}, status=400)

    if (status == 'active'):
        table = actives
    elif (status == 'inactive'):
        table = inactives
    else:
        return json(
            {'message': 'Status "{}" does not exist'.format(status)},
            status=400
        )

    try:
        payload = loads(request.body)
        url = payload['url']

    except KeyError:
        return json({'message': 'Please provide a new url'}, status=400)

    except Exception:
        return json({'message': 'Incorrect payload'}, status=400)

    try:
        async with request.app.engine.acquire() as conn:
            trans = await conn.begin()
            queryset = await conn.execute(
                table.select().where(
                    table.columns['id'] == link_id
                )
            )
            if await queryset.fetchone():
                await conn.execute(
                    table.update().where(
                        table.columns['id'] == link_id
                    ).values(url=url)
                )
                await trans.commit()
                await trans.close()
                return json({'message': 'Link updated'}, status=200)

            await trans.close()
            return json({'message': 'Link does not exist'}, status=404)

    except Exception:
        await trans.close()
        return json({'message': 'Updating link failed'}, status=500)


@api_update_link_blueprint.route(
    '/api/link/<identifier>',
    methods=['PUT']
)
async def api_update_link_by_identifier(request, identifier):
    try:
        token = request.headers['Bearer']
        if (token != config('ACCESS_TOKEN')):
            return json({'message': 'Unauthorized'}, status=401)

    except KeyError:
        return json({'message': 'Please provide a token'}, status=400)

    try:
        payload = loads(request.body)
        url = payload['url']

    except KeyError:
        return json({'message': 'Please provide a new url'}, status=400)

    except Exception:
        return json({'message': 'Incorrect payload'}, status=400)

    try:
        async with request.app.engine.acquire() as conn:
            trans = await conn.begin()
            ac_queryset = await conn.execute(
                actives.select().where(
                    actives.columns['identifier'] == identifier
                )
            )
            ac_data = await ac_queryset.fetchone()
            in_queryset = await conn.execute(
                inactives.select().where(
                    inactives.columns['identifier'] == identifier
                )
            )
            in_data = await in_queryset.fetchone()
            if ac_data:
                table, data = actives, ac_data

            elif in_data:
                table, data = inactives, in_data

            else:
                return json({'message': 'Link does not exist'}, status=404)

            await conn.execute(
                table.update().where(
                    table.columns['id'] == data.id
                ).values(url=url)
            )
            await trans.commit()
            await trans.close()
            return json({'message': 'Link updated'}, status=200)

    except Exception:
        await trans.close()
        return json({'message': 'Updating link failed'}, status=500)
