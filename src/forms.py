'''
Copyright (C) 2020 Link Shortener Authors (see AUTHORS in Documentation).
Licensed under the MIT (Expat) License (see LICENSE in Documentation).
'''
import uuid

from sanic import Blueprint
from sanic.response import redirect, html, json

from sanic_oauth.blueprint import login_required

from sanic_wtf import SanicForm

from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

from initialise_db import initdb_blueprint


forms_blueprint = Blueprint('forms')

actives = initdb_blueprint.active_table
inactives = initdb_blueprint.inactive_table


class CreateForm(SanicForm):
    endpoint = StringField('Endpoint', validators=[DataRequired()])
    url = StringField('URL', validators=[DataRequired()])
    submit = SubmitField('Create')


@forms_blueprint.route('/create', methods=['GET', 'POST'])
@login_required
async def create_link(request, user):
    form = CreateForm(request)
    if request.method == 'POST' and form.validate():
        data = [(
            str(uuid.uuid1())[:36],
            user.email,
            user.id,
            form.endpoint.data,
            form.url.data
        )]
        try:
            async with request.app.engine.acquire() as conn:
                trans = await conn.begin()
                await conn.execute(
                    'INSERT INTO active_links \
                     (identifier, owner, owner_id, endpoint, url) \
                     VALUES (%s, %s, %s, %s, %s)',
                    data
                )
                await trans.commit()
                await trans.close()

                return redirect('/')

        except Exception as error:
            print(error)
            await trans.close()
            return json({'message': 'creating a new link failed'}, status=500)

    content = f"""
    <div class="container">
    <form action="" method="POST">
      <h1 id="form-header">Create a new link</h1>
      {'<br>'.join(form.csrf_token.errors)}
      {form.csrf_token}
      {'<br>'.join(form.endpoint.errors)}
      <br>
      <ul>
      <li>
      {form.endpoint(size=20, placeholder="Endpoint")}
      </li>
      <li>
      {form.url(size=20, placeholder="URL")}
      </li>
      <li>
      {form.submit}
      </li>
      </ul>
    </form>
    """
    base = open('src/templates/base.html', 'r').read()
    appendix = open('src/templates/forms/create_form.html', 'r').read()

    return html(base + content + appendix)
