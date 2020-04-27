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
@credential_whitelist_check
async def create_link_form(request, user):
    form = CreateForm(request)
    return html(template_loader(
                    template_file='create_form.html',
                    form=form
                ), status=200)


@form_blueprint.route('/create', methods=['POST'])
@login_required
@credential_whitelist_check
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
@credential_whitelist_check
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
            link = await query.fetchone()
            return html(template_loader(
                            template_file='edit_form.html',
                            form=form,
                            link=link
                        ), status=200)

    except Exception:
        return json({'message': 'getting update form failed'}, status=500)


@form_blueprint.route('/edit/<status>/<link_id>', methods=['POST'])
@login_required
@credential_whitelist_check
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
