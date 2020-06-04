'''
Copyright (C) 2020 Link Shortener Authors (see AUTHORS in Documentation).
Licensed under the MIT (Expat) License (see LICENSE in Documentation).
'''
from decouple import config
from json import loads
from datetime import date

from sanic import Blueprint
from sanic.response import json

from link_shortener.commands.update import update_link


api_update_blueprint = Blueprint('api_update')


@api_update_blueprint.route('/api/link/<link_id>', methods=['PUT'])
async def api_update_link(request, link_id):
    try:
        token = request.headers['Bearer']
        if (token != config('ACCESS_TOKEN')):
            return json({'message': 'Unauthorized'}, status=401)

    except KeyError:
        return json({'message': 'Please provide a token'}, status=400)

    try:
        data = {'password': None}
        payload = loads(request.body)
        data['url'] = payload['url']
        sd = payload['switch_date']
        data['switch_date'] = date(sd['Year'], sd['Month'], sd['Day'])

        message, status = await update_link(request, link_id, data)
        return json({'message': message}, status=status)

    except KeyError:
        return json({'message': 'Please provide all data'}, status=400)

    except Exception:
        return json({'message': 'Bad request and/or payload'}, status=400)
