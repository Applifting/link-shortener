'''
Copyright (C) 2020 Link Shortener Authors (see AUTHORS in Documentation).
Licensed under the MIT (Expat) License (see LICENSE in Documentation).
'''
import aiohttp

from json import dumps
from decouple import config

from sanic import Sanic, response
from sanic.response import json, text, html

from sanic_oauth.blueprint import oauth_blueprint, login_required

from sanic_session import InMemorySessionInterface

from initialise_db import initdb_blueprint
from authentication import auth_blueprint
from templates import template_blueprint
from forms import forms_blueprint
from routes import route_blueprint

from commands import template_generators


app = Sanic(__name__)

app.blueprint(initdb_blueprint)
app.blueprint(oauth_blueprint)
app.blueprint(auth_blueprint)
app.blueprint(template_blueprint)
app.blueprint(forms_blueprint)
app.blueprint(route_blueprint)

app.static('/', './static')
app.config.WTF_CSRF_SECRET_KEY = config('WTF_CSRF_SECRET_KEY')

actives = initdb_blueprint.active_table
inactives = initdb_blueprint.inactive_table

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
            # request['session']['user_info'] = {'email': user_info.email}
            request['session']['user_info'] = dict(
                [(attr, getattr(user_info, attr))
                  for attr in user_info.default_attrs]
            )
        except AttributeError:
            pass
    except KeyError:
        pass

    await request.app.session_interface.save(request, response)

# ----------------------------------------------------------------------------
# MAIN ROUTES
# ----------------------------------------------------------------------------

@app.route('/db_all', methods=['GET'])
async def db_check(request):
    try:
        async with app.engine.acquire() as conn:
            data = []
            queryset1 = await conn.execute(actives.select())
            for row in await queryset1.fetchall():
                data.append(
                    (
                        row.id,
                        row.identifier,
                        row.owner,
                        row.owner_id,
                        row.endpoint,
                        row.url
                    )
                )
            queryset2 = await conn.execute(inactives.select())
            for row in await queryset2.fetchall():
                data.append(
                    (
                        row.id,
                        row.identifier,
                        row.owner,
                        row.owner_id,
                        row.endpoint,
                        row.url
                    )
                )
            return json(dumps(data), status=200)

    except Exception as error:
        print(error)
        return json({'message': 'getting links failed'}, status=500)



@app.route('/', methods=['GET'])
async def get_active_links(request):
    try:
        async with app.engine.acquire() as conn:
            data = []
            queryset = await conn.execute(actives.select())
            for row in await queryset.fetchall():
                data.append((row.endpoint, row.owner, row.url))

            return html(
                template_generators.all_links_page_generator(data),
                status=200
            )

    except Exception as error:
        print(error)
        return json({'message': 'getting links failed'}, status=500)


@app.route('/my_links', methods=['GET'])
@login_required
async def owner_specific_links(request, user):
    try:
        async with app.engine.acquire() as conn:
            ac_data, in_data = [], []
            ac_queryset = await conn.execute(
                actives.select().where(
                    actives.columns['owner_id'] == user.id
                )
            )
            in_queryset = await conn.execute(
                inactives.select().where(
                    inactives.columns['owner_id'] == user.id
                )
            )
            for row in await ac_queryset.fetchall():
                ac_data.append((row.endpoint, row.url))

            for row in await in_queryset.fetchall():
                in_data.append((row.endpoint, row.url))

            return html(
                template_generators.my_links_page_generator(ac_data, in_data),
                status=200
            )

    except Exception as error:
        print(error)
        return json({'message': 'getting your links failed'}, status=500)


@app.route('/<link_endpoint>', methods=['GET'])
async def redirect_link(request, link_endpoint):
    try:
        async with app.engine.acquire() as conn:
            query = await conn.execute(
                actives.select().where(
                    actives.columns['endpoint'] == link_endpoint
                )
            )
            url = await query.fetchone()
            return response.redirect(url.url)

    except Exception as error:
        print(error)
        return json({'message': 'link inactive or does not exist'}, status=400)


if (__name__ == '__main__'):
    app.run(host='0.0.0.0', port=8000)
