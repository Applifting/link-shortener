'''
Copyright (C) 2020 Link Shortener Authors (see AUTHORS in Documentation).
Licensed under the MIT (Expat) License (see LICENSE in Documentation).
'''
from decouple import config

from sanic import Blueprint
from sanic.response import json

from link_shortener.commands.switch import activate_link, deactivate_link


api_switch_blueprint = Blueprint('api_switch')


@api_switch_blueprint.route('/api/activate/<link_id>', methods=['GET'])
async def api_activate_link(request, link_id):
    try:
        token = request.headers['Bearer']
        if (token != config('ACCESS_TOKEN')):
            return json({'message': 'Unauthorized'}, status=401)

    except KeyError:
        return json({'message': 'Please provide a token'}, status=400)

    message, status = await activate_link(request, link_id)
    return json({'message': message}, status=status)


@api_switch_blueprint.route('/api/deactivate/<link_id>', methods=['GET'])
async def api_deactivate_link(request, link_id):
    try:
        token = request.headers['Bearer']
        if (token != config('ACCESS_TOKEN')):
            return json({'message': 'Unauthorized'}, status=401)

    except KeyError:
        return json({'message': 'Please provide a token'}, status=400)

    message, status = await deactivate_link(request, link_id)
    return json({'message': message}, status=status)
