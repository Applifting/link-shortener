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
        payload = loads(request.body)
        for column in ('owner', 'owner_id', 'endpoint', 'url'):
            value = payload.get(column, None)
            if not value:
                missing = column
                raise MissingDataException
            if not isinstance(value, str):
                raise IncorrectDataFormat

        data = {'password': None}
        data['owner'] = payload['owner']
        data['owner_id'] = payload['owner_id']
        data['endpoint'] = payload['endpoint']
        data['url'] = payload['url']
        if payload.get('switch_date', None):
            sd = payload['switch_date']
            try:
                data['switch_date'] = date(
                    sd['Year'],
                    sd['Month'],
                    sd['Day']
                )
            except (KeyError, TypeError):
                raise IncorrectDataFormat
        else:
            data['switch_date'] = None

        await create_link(request, data=data)
        status, message = 201, 'Link created successfully'
    except AccessDeniedException:
        status, message = 401, 'Unauthorized'
    except JSONDecodeError:
        status, message = 400, 'Please provide data in JSON format'
    except MissingDataException:
        status = 400
        message = 'Please provide all data. Missing: {}'.format(missing)
    except IncorrectDataFormat:
        status, message = 400, 'Please provide correctly formatted data'
    except DuplicateActiveLinkForbidden:
        status, message = 409, 'An active link with that name already exists'
    finally:
        return json({'message': message}, status=status)
