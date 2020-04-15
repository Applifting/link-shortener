'''
Copyright (C) 2020 Link Shortener Authors
Licensed under the MIT (Expat) License. See the LICENSE file found in the
top-level directory of this distribution.
'''
import aiohttp

from json import dumps
from decouple import config

from sanic import Sanic, response
from sanic.response import json, text

from sanic_oauth.blueprint import oauth_blueprint, login_required

from sanic_session import InMemorySessionInterface

from initialise_db import initdb_blueprint
from authentication import auth_blueprint


app = Sanic(__name__)

app.blueprint(initdb_blueprint)
app.blueprint(oauth_blueprint)
app.blueprint(auth_blueprint)

table = initdb_blueprint.table

# ----------------------------------------------------------------------------
# AUTHENTICATION
# ----------------------------------------------------------------------------

app.session_interface = InMemorySessionInterface()
app.config.OAUTH_PROVIDER = config('OAUTH_PROVIDER')
app.config.OAUTH_REDIRECT_URI = config('OAUTH_REDIRECT_URI')
app.config.OAUTH_SCOPE = config('OAUTH_SCOPE')
app.config.OAUTH_CLIENT_ID = config('OAUTH_CLIENT_ID')
app.config.OAUTH_CLIENT_SECRET = config('OAUTH_CLIENT_SECRET')


@app.middleware('request')
async def add_session_to_request(request):
    await request.app.session_interface.open(request)


@app.middleware('response')
async def save_session(request, response):
    '''
    See SESSION_ERROR in Documentation.
    '''
    try:
        user_info = request['session']['user_info']
        try:
            request['session']['user_info'] = dict(
                [(attr, getattr(user_info, attr))
                  for attr in user_info.default_attrs]
            )
        except AttributeError:
            pass
    except KeyError:
        pass

    await request.app.session_interface.save(request, response)


@app.route('/profile')
@login_required
async def user_profile(request, user):
    data = 'User: {}'.format(user.email)
    return response.text(data)

# ----------------------------------------------------------------------------
# MAIN ROUTES
# ----------------------------------------------------------------------------

@app.route('/', methods=['GET'])
async def get_active_links(request):
    try:
        async with app.engine.acquire() as conn:
            data = ''
            queryset = await conn.execute(
                table.select().where(
                    table.columns['is_active'] == True
                )
            )
            for row in await queryset.fetchall():
                data += 'Owner: {}\nEndpoint: {} \nURL: {} \n\n'.format(
                    row.owner, row.endpoint, row.url
                )
            return text(data, status=200)

    except Exception as error:
        print(error)
        return json({'message': 'getting links failed'}, status=500)


@app.route('/my_links', methods=['GET'])
@login_required
async def owner_specific_links(request, user):
    try:
        async with app.engine.acquire() as conn:
            data = 'User: {}\n\n'.format(user.email)
            queryset = await conn.execute(
                table.select().where(
                    table.columns['owner'] == user.email
                )
            )
            for row in await queryset.fetchall():
                data += 'Endpoint: {} \nURL: {} \nActive: {}\n\n'.format(
                    row.endpoint, row.url, row.is_active
                )
            return text(data, status=200)

    except Exception as error:
        print(error)
        return json({'message': 'getting your links failed'}, status=500)


@app.route('/<link_endpoint>', methods=['GET'])
async def redirect_link(request, link_endpoint):
    try:
        async with app.engine.acquire() as conn:
            query = await conn.execute(
                table.select().where(
                    table.columns['endpoint'] == link_endpoint
                )
            )
            url = await query.fetchone()
            return response.redirect(url[2])

    except Exception as error:
        print(error)
        return json({'message': 'link does not exist'}, status=400)


if (__name__ == '__main__'):
    app.run(host='0.0.0.0', port=8000)
