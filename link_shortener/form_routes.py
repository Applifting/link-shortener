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

from link_shortener.models import actives, inactives
from link_shortener.templates import template_loader

from link_shortener.core.decorators import credential_whitelist_check


form_blueprint = Blueprint('forms')


class CreateForm(SanicForm):
    endpoint = StringField('Endpoint', validators=[DataRequired()])
    url = StringField('URL', validators=[DataRequired()])
    submit = SubmitField('Create')


class UpdateForm(SanicForm):
    url = StringField('URL', validators=[DataRequired()])
    submit = SubmitField('Update')


@form_blueprint.route('/create', methods=['GET'])
@login_required
@credential_whitelist_check()
async def create_link_form(request, user):
    form = CreateForm(request)
    content = f"""
        <div class="container">
        <form action="" method="POST">
          <h1 id="form-header">Create a new link</h1>
          {'<br>'.join(form.csrf_token.errors)}
          {form.csrf_token}
          {'<br>'.join(form.endpoint.errors)}
          <br>
          <ul>
          <li>{form.endpoint(size=20, placeholder="Endpoint")}</li>
          <li>{form.url(size=20, placeholder="URL")}</li>
          <li>{form.submit}</li>
          </ul>
        </form>
    """
    return html(template_loader(
                    template_file='wtf_form.html',
                    form=content
                ), status=200)


@form_blueprint.route('/create', methods=['POST'])
@login_required
@credential_whitelist_check()
async def create_link_save(request, user):
    form = CreateForm(request)
    if not form.validate():
        return json({'message': 'form invalid'}, status=400)

    try:
        async with request.app.engine.acquire() as conn:
            trans = await conn.begin()
            await conn.execute(
                actives.insert().values(
                    identifier=str(uuid.uuid1()),
                    owner=user.email,
                    owner_id=user.id,
                    endpoint=form.endpoint.data,
                    url=form.url.data
                )
            )
            await trans.commit()
            await trans.close()
            return redirect('/links/me')

    except Exception:
        await trans.close()
        return json(
            {'message': 'an active link with that endpoint already exists'},
            status=500
        )


@form_blueprint.route('/edit/<status>/<link_id>', methods=['GET'])
@login_required
@credential_whitelist_check()
async def update_link_form(request, user, status, link_id):
    form = UpdateForm(request)
    if (status == 'active'):
        table = actives
    elif (status == 'inactive'):
        table = inactives
    else:
        return json({'message': 'path does not exist'}, status=400)

    try:
        async with request.app.engine.acquire() as conn:
            query = await conn.execute(
                table.select().where(
                    table.columns['id'] == link_id
                )
            )
            row = await query.fetchone()
            content = f"""
                <div class="container">
                <form action="" method="POST">
                  <h1 id="form-header">/{row.endpoint}</h1>
                  {'<br>'.join(form.csrf_token.errors)}
                  {form.csrf_token}
                  {'<br>'.join(form.url.errors)}
                  <br>
                  <ul>
                  <li>{form.url(size=50, placeholder=row.url)}</li>
                  <li>{form.submit}</li>
                  </ul>
                </form>
            """
            return html(template_loader(
                            template_file='wtf_form.html',
                            form=content
                        ), status=200)

    except Exception:
        return json({'message': 'getting update form failed'}, status=500)


@form_blueprint.route('/edit/<status>/<link_id>', methods=['POST'])
@login_required
@credential_whitelist_check()
async def update_link_save(request, user, status, link_id):
    form = UpdateForm(request)
    if (status == 'active'):
        table = actives
    elif (status == 'inactive'):
        table = inactives
    else:
        return json({'message': 'path does not exist'}, status=400)

    if not form.validate():
        return json({'message': 'form invalid'}, status=400)

    try:
        async with request.app.engine.acquire() as conn:
            trans = await conn.begin()
            await conn.execute(
                table.update().where(
                    table.columns['id'] == link_id
                ).values(
                    url=form.url.data
                )
            )
            await trans.commit()
            await trans.close()
            return redirect('/links/me')

    except Exception as error:
        print(error)
        await trans.close()
        return json({'message': 'updating link failed'}, status=500)
