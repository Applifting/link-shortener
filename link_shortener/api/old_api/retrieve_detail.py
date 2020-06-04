'''
Copyright (C) 2020 Link Shortener Authors (see AUTHORS in Documentation).
Licensed under the MIT (Expat) License (see LICENSE in Documentation).
'''
from json import dumps
from decouple import config

from sanic import Blueprint
from sanic.response import json

from link_shortener.models import links

from link_shortener.commands.retrieve import retrieve_link


api_retrieve_detail_blueprint = Blueprint('retrieve_detail')


@api_retrieve_detail_blueprint.route('/api/link/<link_id>', methods=['GET'])
async def api_link_detail_by_id(request, link_id):
    try:
        token = request.headers['Bearer']
        if (token != config('ACCESS_TOKEN')):
            return json({'message': 'Unauthorized'}, status=401)

    except KeyError:
        return json({'message': 'Please provide a token'}, status=400)

    try:
        link_data, status = await retrieve_link(request, link_id)
        if status:
            return json({'message': link_data}, status=status)

        data = {
            'id': link_data.id,
            'owner': link_data.owner,
            'owner_id': link_data.owner_id,
            'endpoint': link_data.endpoint,
            'url': link_data.url,
            'switch_date': {
                'Year': link_data.switch_date['Year'],
                'Month': link_data.switch_date['Month'],
                'Day': link_data.switch_date['Day']
            },
            'is_active': link_data.is_active
        }
        return json(dumps(data), status=200)

    except Exception as error:
        print(error)
        return json({'message': 'Getting link failed'}, status=500)

    # try:
    #     async with request.app.engine.acquire() as conn:
    #         queryset = await conn.execute(
    #             table.select().where(
    #                 table.columns['id'] == link_id
    #             )
    #         )
    #         try:
    #             link_data = await queryset.fetchone()
    #             data = {
    #                 'id': link_data.id,
    #                 'identifier': link_data.identifier,
    #                 'owner': link_data.owner,
    #                 'owner_id': link_data.owner_id,
    #                 'endpoint': link_data.endpoint,
    #                 'url': link_data.url,
    #             }
    #             return json(dumps(data), status=200)
    #
    #         except Exception:
    #             return json({'message': 'Link does not exist'}, status=404)
    #
    # except Exception:
    #     return json({'message': 'Getting link failed'}, status=500)
