'''
Copyright (C) 2020 Link Shortener Authors (see AUTHORS in Documentation).
Licensed under the MIT (Expat) License (see LICENSE in Documentation).
'''
from datetime import date
from decouple import config
from json import loads

from sanic import Blueprint
from sanic.response import json

from link_shortener.commands.create import create_link


api_create_blueprint = Blueprint('api_create')


@api_create_blueprint.route('/api/links', methods=['POST'])
async def api_create_link(request):
    try:
        token = request.headers['Bearer']
        if (token != config('ACCESS_TOKEN')):
            return json({'message': 'Unauthorized'}, status=401)

    except KeyError:
        return json({'message': 'Please provide a token'}, status=400)

    try:
        data = {'password': None}
        payload = loads(request.body)
        data['owner'] = payload['owner']
        data['owner_id'] = payload['owner_id']
        data['endpoint'] = payload['endpoint']
        data['url'] = payload['url']
        sd = payload['switch_date']
        data['switch_date'] = date(sd['Year'], sd['Month'], sd['Day'])

        message, status = await create_link(request, data)
        return json({'message': message}, status=status)

    except KeyError:
        return json({'message': 'Please provide all data'}, status=400)

    except Exception:
        return json({'message': 'Bad request and/or payload'}, status=400)
