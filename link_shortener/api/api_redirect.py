'''
Copyright (C) 2020 Link Shortener Authors (see AUTHORS in Documentation).
Licensed under the MIT (Expat) License (see LICENSE in Documentation).
'''
from sanic import Blueprint
from sanic.response import json

from link_shortener.commands.redirect import redirect_link
from link_shortener.commands.authorize import check_token
from link_shortener.core.exceptions import (AccessDeniedException,
                                            NotFoundException)


api_redirect_blueprint = Blueprint('api_redirect')


@api_redirect_blueprint.route('/api/<link_endpoint>', methods=['GET'])
async def api_redirect_link(request, link_endpoint):
    try:
        await check_token(request)
        target_url = await redirect_link(request, link_endpoint)
        status, response = 200, {'endpoint': link_endpoint, 'url': target_url}
    except AccessDeniedException:
        status, response = 401, {'message': 'Unauthorized'}
    except NotFoundException:
        status, response = 404, {'message': 'Link inactive or does not exist'}
    finally:
        return json(response, status=status)
