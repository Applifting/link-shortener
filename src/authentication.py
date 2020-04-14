'''
Copyright (C) 2020 Link Shortener Authors
Licensed under the MIT (Expat) License. See the LICENSE file found in the
top-level directory of this distribution.
'''
import aiohttp

from sanic import Blueprint, response


auth_blueprint = Blueprint('authentication')


@auth_blueprint.listener('before_server_start')
async def init_aiohttp_session(sanic_app, _loop) -> None:
    sanic_app.async_session = aiohttp.ClientSession()


@auth_blueprint.listener('after_server_stop')
async def close_aiohttp_session(sanic_app, _loop) -> None:
    await sanic_app.async_session.close()


@auth_blueprint.route('/redirect', methods=['GET'])
async def redirected_page(request):
    return response.text('Successfully logged in!')
