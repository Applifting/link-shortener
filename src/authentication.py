'''
Copyright (C) 2020 Link Shortener Authors (see AUTHORS in Documentation).
Licensed under the MIT (Expat) License (see LICENSE in Documentation).
'''
import aiohttp

from sanic import Blueprint, response

from sanic_oauth.blueprint import login_required


auth_blueprint = Blueprint('authentication')


@auth_blueprint.listener('before_server_start')
async def init_aiohttp_session(sanic_app, _loop) -> None:
    sanic_app.async_session = aiohttp.ClientSession()


@auth_blueprint.listener('after_server_stop')
async def close_aiohttp_session(sanic_app, _loop) -> None:
    await sanic_app.async_session.close()


@auth_blueprint.route('/profile')
@login_required
async def user_profile(request, user):
    data = 'User: {}'.format(user.email)
    return response.text(data)
