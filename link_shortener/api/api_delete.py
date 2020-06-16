'''
Copyright (C) 2020 Link Shortener Authors (see AUTHORS in Documentation).
Licensed under the MIT (Expat) License (see LICENSE in Documentation).
'''
from decouple import config

from sanic import Blueprint
from sanic.response import json

from link_shortener.commands.delete import delete_link
from link_shortener.commands.authorize import check_token

from link_shortener.core.exceptions import (AccessDeniedException,
                                            NotFoundException)


api_delete_blueprint = Blueprint('api_delete')


@api_delete_blueprint.route('/api/link/<link_id>', methods=['DELETE'])
async def api_delete_link(request, link_id):
    try:
        await check_token(request)
        await delete_link(request, link_id)
        return json({'message': 'Link deleted successfully'}, status=200)
    except AccessDeniedException:
        return json({'message': 'Unauthorized'}, status=401)
    except NotFoundException:
        return json({'message': 'Link does not exist'}, status=404)
