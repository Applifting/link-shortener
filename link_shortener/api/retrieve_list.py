'''
Copyright (C) 2020 Link Shortener Authors (see AUTHORS in Documentation).
Licensed under the MIT (Expat) License (see LICENSE in Documentation).
'''
from json import dumps
from decouple import config

from sanic import Blueprint
from sanic.response import json

from link_shortener.models import actives, inactives


api_retrieve_list_blueprint = Blueprint('retrieve_list')


@api_retrieve_list_blueprint.route('/api/links', methods=['GET'])
async def api_link_list(request):
    try:
        token = request.headers['Bearer']
        if (token != config('ACCESS_TOKEN')):
            return json({'message': 'Unauthorized'}, status=401)

    except KeyError:
        return json({'message': 'Please provide a token'}, status=400)

    try:
        async with request.app.engine.acquire() as conn:
            data = []
            queryset1 = await conn.execute(actives.select())
            for row in await queryset1.fetchall():
                data.append(
                    (
                        row.id,
                        row.identifier,
                        row.owner,
                        row.owner_id,
                        row.endpoint,
                        row.url
                    )
                )
            queryset2 = await conn.execute(inactives.select())
            for row in await queryset2.fetchall():
                data.append(
                    (
                        row.id,
                        row.identifier,
                        row.owner,
                        row.owner_id,
                        row.endpoint,
                        row.url
                    )
                )
            return json(dumps(data), status=200)

    except Exception:
        return json({'message': 'Getting links failed'}, status=500)
