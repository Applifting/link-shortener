'''
Copyright (C) 2020 Link Shortener Authors (see AUTHORS in Documentation).
Licensed under the MIT (Expat) License (see LICENSE in Documentation).
'''
from sanic import Blueprint
from sanic.response import json

from link_shortener.commands.retrieve import retrieve_links, retrieve_link
from link_shortener.commands.authorize import check_token

from link_shortener.core.exceptions import (AccessDeniedException,
                                            NotFoundException)


api_retrieve_blueprint = Blueprint('api_retrieve')


@api_retrieve_blueprint.route('/api/links', methods=['GET'])
async def api_retrieve_links(request):
    try:
        await check_token(request)
        link_data = await retrieve_links(request, filters={})
        return json(link_data, status=200)
    except AccessDeniedException:
        return json({'message': 'Unauthorized'}, status=401)


@api_retrieve_blueprint.route('/api/link/<link_id>', methods=['GET'])
async def api_retrieve_link(request, link_id):
    try:
        await check_token(request)
        link = await retrieve_link(request, link_id)
        return json(link, status=200)
    except AccessDeniedException:
        return json({'message': 'Unauthorized'}, status=401)
    except NotFoundException:
        return json({'message': 'Link does not exist'}, status=404)
