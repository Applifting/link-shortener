'''
Copyright (C) 2020 Link Shortener Authors (see AUTHORS in Documentation).
Licensed under the MIT (Expat) License (see LICENSE in Documentation).
'''
from json import loads
from json.decoder import JSONDecodeError
from datetime import date

from sanic import Blueprint
from sanic.response import json

from link_shortener.commands.update import update_link
from link_shortener.commands.authorize import check_token

from link_shortener.core.exceptions import (AccessDeniedException,
                                            DuplicateActiveLinkForbidden,
                                            IncorrectDataFormat,
                                            LinkNotAllowed,
                                            MissingDataException,
                                            NotFoundException)


api_update_blueprint = Blueprint('api_update')


@api_update_blueprint.route('/api/link/<link_id>', methods=['PUT'])
async def api_update_link(request, link_id):
    try:
        await check_token(request)
        payload = loads(request.body)

        url, endpoint = payload.get('url', None), payload.get('endpoint', None)
        if not (url or endpoint):
            raise MissingDataException

        is_url_string = isinstance(url, (str, type(None)))
        is_endpoint_string = isinstance(endpoint, (str, type(None)))
        if not (is_url_string and is_endpoint_string):
            raise IncorrectDataFormat

        api_data = {'password': None, 'url': url, 'endpoint': endpoint}
        if payload.get('switch_date', None):
            try:
                api_data['switch_date'] = date(
                    payload['switch_date']['Year'],
                    payload['switch_date']['Month'],
                    payload['switch_date']['Day']
                )
            except (KeyError, TypeError):
                raise IncorrectDataFormat
        else:
            api_data['switch_date'] = None

        await update_link(request, link_id=link_id, data=api_data)
        status, message = 200, 'Link updated successfully'
    except AccessDeniedException:
        status, message = 401, 'Unauthorized'
    except JSONDecodeError:
        status, message = 400, 'Please provide data in JSON format'
    except MissingDataException:
        status = 400
        message = 'Please provide all data. Missing: url and/or endpoint'
    except IncorrectDataFormat:
        status, message = 400, 'Please provide correctly formatted data'
    except NotFoundException:
        status, message = 404, 'Link does not exist'
    except DuplicateActiveLinkForbidden:
        status, message = 409, 'An active link with that name already exists'
    except LinkNotAllowed:
        status, message = 400, 'The provided link URL is blacklisted'
    finally:
        return json({'message': message}, status=status)
