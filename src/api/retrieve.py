'''
Copyright (C) 2020 Link Shortener Authors (see AUTHORS in Documentation).
Licensed under the MIT (Expat) License (see LICENSE in Documentation).
'''
from json import dumps

from sanic import Blueprint
from sanic.response import json

from sanic_oauth.blueprint import login_required

from models import actives, inactives


api_retrieve_blueprint = Blueprint('retrieve')


@api_retrieve_blueprint.route('/get_links', methods=['GET'])
@login_required
async def get_links(request, user):
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
