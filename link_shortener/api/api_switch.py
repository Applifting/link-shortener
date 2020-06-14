'''
Copyright (C) 2020 Link Shortener Authors (see AUTHORS in Documentation).
Licensed under the MIT (Expat) License (see LICENSE in Documentation).
'''
from aiomysql.sa.exc import InvalidRequestError

from sanic import Blueprint
from sanic.response import json

from link_shortener.commands.switch import activate_link, deactivate_link
from link_shortener.commands.authorize import check_token

from link_shortener.core import exceptions as exc


api_switch_blueprint = Blueprint('api_switch')


@api_switch_blueprint.route('/api/activate/<link_id>', methods=['GET'])
async def api_activate_link(request, link_id):
    try:
        await check_token(request)
        await activate_link(request, link_id)
        status, message = 200, 'Link activated successfully'
    except exc.AccessDeniedException:
        status, message = 401, 'Unauthorized'
    except InvalidRequestError:
        status, message = 404, 'Link does not exist'
    except exc.DuplicateActiveLinkForbidden:
        status, message = 400, 'An active link with that name already exists'
    finally:
        return json({'message': message}, status=status)


@api_switch_blueprint.route('/api/deactivate/<link_id>', methods=['GET'])
async def api_deactivate_link(request, link_id):
    try:
        await check_token(request)
        await deactivate_link(request, link_id)
        status, message = 200, 'Link deactivated successfully'
    except exc.AccessDeniedException:
        status, message = 401, 'Unauthorized'
    except InvalidRequestError:
        status, message = 404, 'Link does not exist'
    finally:
        return json({'message': message}, status=status)
