'''
Copyright (C) 2020 Link Shortener Authors (see AUTHORS in Documentation).
Licensed under the MIT (Expat) License (see LICENSE in Documentation).
'''
from decouple import config

from sanic import Blueprint
from sanic.response import json

from link_shortener.commands.retrieve import retrieve_links, retrieve_link
from link_shortener.commands.authorize import check_token


api_retrieve_blueprint = Blueprint('api_retrieve')


@api_retrieve_blueprint.route('/api/links', methods=['GET'])
async def api_retrieve_links(request):
    if await check_token(request):
        message, status = await check_token(request)
        return json({'message': message}, status=status)

    try:
        data = []
        for link in await retrieve_links(request, {}):
            link_data = {
                'id': link.id,
                'owner': link.owner,
                'endpoint': link.endpoint,
                'url': link.url,
                'is_active': link.is_active
            }
            if link.switch_date:
                link_data['switch_date'] = {
                    'Year': link.switch_date.year,
                    'Month': link.switch_date.month,
                    'Day': link.switch_date.day
                }

            data.append(link_data)

        return json(data, status=200)

    except Exception as error:
        print(error)
        return json({'message': 'Getting links failed'}, status=500)


@api_retrieve_blueprint.route('/api/link/<link_id>', methods=['GET'])
async def api_retrieve_link(request, link_id):
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
            'is_active': link_data.is_active
        }
        if link_data.switch_date:
            data['switch_date'] = {
                'Year': link_data.switch_date.year,
                'Month': link_data.switch_date.month,
                'Day': link_data.switch_date.day
            }

        return json(data, status=200)

    except Exception:
        return json({'message': 'Getting link failed'}, status=500)
