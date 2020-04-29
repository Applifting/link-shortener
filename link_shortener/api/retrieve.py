'''
Copyright (C) 2020 Link Shortener Authors (see AUTHORS in Documentation).
Licensed under the MIT (Expat) License (see LICENSE in Documentation).
'''
from json import dumps
from decouple import config

from sanic import Blueprint
from sanic.response import json

from sanic_oauth.blueprint import login_required

from link_shortener.models import actives, inactives
from link_shortener.core.decorators import credential_whitelist_check


api_retrieve_blueprint = Blueprint('retrieve')


@api_retrieve_blueprint.route('/api/links', methods=['GET'])
async def get_links(request):
    if (request.headers['Bearer'] != config('ACCESS_TOKEN')):
        return json({'message': 'Unauthorized'}, status=401)

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

    except Exception as error:
        print(error)
        return json({'message': 'getting links failed'}, status=500)
