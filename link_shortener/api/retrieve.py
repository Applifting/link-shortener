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
async def get_all_links(request):
    try:
        token = request.headers['Bearer']
        if (token != config('ACCESS_TOKEN')):
            return json({'message': 'Unauthorized'}, status=401)

    except KeyError:
        return json({'message': 'please provide a token'}, status=400)

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
        return json({'message': 'getting links failed'}, status=500)


@api_retrieve_blueprint.route('/api/links/<status>/<link_id>', methods=['GET'])
async def get_link_detail(request, status, link_id):
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
        token = request.headers['Bearer']
        if (token != config('ACCESS_TOKEN')):
            return json({'message': 'Unauthorized'}, status=401)

    except KeyError:
        return json({'message': 'please provide a token'}, status=400)

    try:
        async with request.app.engine.acquire() as conn:
            queryset = await conn.execute(
                table.select().where(
                    table.columns['id'] == link_id
                )
            )
            try:
                link_data = await queryset.fetchone()
                data = {
                    'id': link_data.id,
                    'identifier': link_data.identifier,
                    'owner': link_data.owner,
                    'owner_id': link_data.owner_id,
                    'endpoint': link_data.endpoint,
                    'url': link_data.url,
                    'status': status
                }
                return json(dumps(data), status=200)

            except Exception:
                return json({'message': 'link does not exist'}, status=404)

    except Exception:
        return json({'message': 'getting link failed'}, status=500)
