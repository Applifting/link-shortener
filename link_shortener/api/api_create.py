'''
Copyright (C) 2020 Link Shortener Authors (see AUTHORS in Documentation).
Licensed under the MIT (Expat) License (see LICENSE in Documentation).
'''
from json import loads

from sanic import Blueprint
from sanic.response import json

from link_shortener.commands.create import create_link
from link_shortener.commands.authorize import check_token

from link_shortener.core.exceptions import (AccessDeniedException,
                                            DuplicateActiveLinkForbidden,
                                            IncorrectDataFormat,
                                            MissingDataException)


api_create_blueprint = Blueprint('api_create')


@api_create_blueprint.route('/api/links', methods=['POST'])
async def api_create_link(request):
    try:
        await check_token(request)
        await create_link(request, data=loads(request.body))
        status, message = 201, 'Link created successfully'
    except AccessDeniedException:
        status, message = 401, 'Unauthorized'
    except MissingDataException:
        status, message = 400, 'Please provide all data'
    except IncorrectDataFormat:
        status, message = 400, 'Please provide correctly formatted data'
    except DuplicateActiveLinkForbidden:
        status, message = 409, 'An active link with that name already exists'
    finally:
        return json({'message': message}, status=status)
