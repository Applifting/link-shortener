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

    except KeyError:
        return json({'message': 'Incorrect payload'}, status=400)

    try:
        async with request.app.engine.acquire() as conn:
            trans = await conn.begin()
            try:
                await conn.execute(
                    table.update().where(
                        table.columns['id'] == link_id
                    ).values(
                        url=url
                    )
                )
                await trans.commit()
                await trans.close()
                return json({'message': 'Link updated'}, status=200)

            except Exception:
                await trans.close()
                return json({'message': 'Link does not exist'}, status=404)


    except Exception:
        return json({'message': 'Updating link failed'}, status=500)
