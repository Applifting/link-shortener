'''
Copyright (C) 2020 Link Shortener Authors (see AUTHORS in Documentation).
Licensed under the MIT (Expat) License (see LICENSE in Documentation).
'''
from json import loads
from json.decoder import JSONDecodeError
from datetime import date

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
        r_body = request.body
        payload = loads(r_body)
        if not isinstance(payload['endpoint'], str):
            raise TypeError

        data = {'password': None}
        data['owner'] = payload['owner']
        data['owner_id'] = payload['owner_id']
        data['endpoint'] = payload['endpoint']
        data['url'] = payload['url']
        if payload['switch_date'] is not None:
            sd = payload['switch_date']
            data['switch_date'] = date(sd['Year'], sd['Month'], sd['Day'])
        else:
            data['switch_date'] = None

        await create_link(request, data=data)
        status, message = 201, 'Link created successfully'
    except AccessDeniedException:
        status, message = 401, 'Unauthorized'
    except JSONDecodeError:
        status, message = 400, 'Please provide data in JSON format'
    except KeyError:
        status, message = 400, 'Please provide all data'
    except TypeError:
        status, message = 400, 'Please provide correctly formatted data'
    except DuplicateActiveLinkForbidden:
        status, message = 409, 'An active link with that name already exists'
    finally:
        return json({'message': message}, status=status)
