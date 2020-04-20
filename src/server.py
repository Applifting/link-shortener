'''
Copyright (C) 2020 Link Shortener Authors (see AUTHORS in Documentation).
Licensed under the MIT (Expat) License (see LICENSE in Documentation).
'''
from decouple import config

from sanic import Sanic
from sanic.response import redirect, json

from sanic_oauth.blueprint import oauth_blueprint

from sanic_session import InMemorySessionInterface

from initialise_db import initdb_blueprint
from authentication import auth_blueprint
from templates import template_blueprint
from forms import forms_blueprint
from views import view_blueprint

from api.retrieve import api_retrieve_blueprint


app = Sanic(__name__)

app.blueprint(initdb_blueprint)
app.blueprint(oauth_blueprint)
app.blueprint(auth_blueprint)
app.blueprint(template_blueprint)
app.blueprint(forms_blueprint)
app.blueprint(view_blueprint)

app.blueprint(api_retrieve_blueprint)

app.static('/links/plus.png', '/app/static/plus.png', name='plus_png')
app.static('/links/edit.png', '/app/static/edit.png', name='edit_png')
app.static('/static', './static')
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
                [
                    (attr, getattr(user_info, attr))
                    for attr in user_info.default_attrs
                ]
            )
        except AttributeError:
            pass
    except KeyError:
        pass

    await request.app.session_interface.save(request, response)

# ----------------------------------------------------------------------------
# MAIN ROUTE
# ----------------------------------------------------------------------------


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
            return redirect(url.url)

    except Exception as error:
        print(error)
        return json({'message': 'link inactive or does not exist'}, status=400)


if (__name__ == '__main__'):
    app.run(host='0.0.0.0', port=8000)
