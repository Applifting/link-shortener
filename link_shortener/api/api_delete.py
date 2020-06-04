'''
Copyright (C) 2020 Link Shortener Authors (see AUTHORS in Documentation).
Licensed under the MIT (Expat) License (see LICENSE in Documentation).
'''
from decouple import config

from sanic import Blueprint
from sanic.response import json

from link_shortener.commands.delete import delete_link


api_delete_blueprint = Blueprint('api_delete')


@api_delete_blueprint.route('/api/link/<link_id>', methods=['DELETE'])
async def api_delete_link(request, link_id):
    try:
        token = request.headers['Bearer']
        if (token != config('ACCESS_TOKEN')):
            return json({'message': 'Unauthorized'}, status=401)

    except KeyError:
        return json({'message': 'Please provide a token'}, status=400)

    message, status = await delete_link(request, link_id)
    return json({'message': message}, status=status)
