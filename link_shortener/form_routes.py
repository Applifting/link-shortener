'''
Copyright (C) 2020 Link Shortener Authors (see AUTHORS in Documentation).
Licensed under the MIT (Expat) License (see LICENSE in Documentation).
'''
import os
import uuid
import hashlib

from sanic import Blueprint
from sanic.response import redirect, html, json

from sanic_oauth.blueprint import login_required

from sanic_wtf import SanicForm

from wtforms import StringField, SubmitField, PasswordField, DateField
from wtforms.validators import DataRequired

from link_shortener.models import links, salts
from link_shortener.templates import template_loader

from link_shortener.commands.authorize import check_form, check_password

from link_shortener.core.decorators import credential_whitelist_check


form_blueprint = Blueprint('forms')


class CreateForm(SanicForm):
    endpoint = StringField('Endpoint', validators=[DataRequired()])
    url = StringField('URL', validators=[DataRequired()])
    password = PasswordField('Password')
    switch_date = DateField('Status switch date')
    submit = SubmitField('Create')


class UpdateForm(SanicForm):
    url = StringField('URL', validators=[])
    password = PasswordField('Password', validators=[])
    switch_date = DateField('Status switch date')
    submit = SubmitField('Update')


class PasswordForm(SanicForm):
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')


@form_blueprint.route('/authorize/<link_id>', methods=['GET'])
async def link_password_form(request, link_id):
    form = PasswordForm(request)
    file, payload, status = await check_form(request, link_id)
    return html(template_loader(
                    template_file=file,
                    form=form,
                    payload=payload,
                    status_code=str(status)
                ), status=status)


@form_blueprint.route('/authorize/<link_id>', methods=['POST'])
async def link_password_save(request, link_id):
    form = PasswordForm(request)
    if not form.validate():
        return html(template_loader(
                        template_file='message.html',
                        payload='Form invalid',
                        status_code='400'
                    ), status=400)

    payload, status = await check_password(request, link_id, form)
    if status:
        return html(template_loader(
                        template_file='message.html',
                        payload=payload,
                        status_code=str(status)
                    ), status=status)

    return redirect(payload, status=302)


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
        return json({'message': 'Form invalid'}, status=400)

    try:
        async with request.app.engine.acquire() as conn:
            trans = await conn.begin()
            try:
                query = await conn.execute(
                    links.select().where(
                        links.columns['endpoint'] == form.endpoint.data
                    ).where(
                        links.columns['is_active'] == True
                    )
                )
                link_data = await query.fetchone()
                if link_data:
                    raise Exception

            except Exception:
                await trans.close()
                return json(
                    {'message': 'This active endpoint already exists'},
                    status=400
                )

            identifier = str(uuid.uuid1())
            if form.password.data:
                salt = os.urandom(32)
                password = hashlib.pbkdf2_hmac(
                    'sha256',
                    form.password.data.encode('utf-8'),
                    salt,
                    100000
                )
                await conn.execute(
                    salts.insert().values(
                        identifier=identifier,
                        salt=salt
                    )
                )
            else:
                password = None

            await conn.execute(
                links.insert().values(
                    identifier=identifier,
                    owner=user.email,
                    owner_id=user.id,
                    password=password,
                    endpoint=form.endpoint.data,
                    url=form.url.data,
                    switch_date=form.switch_date.data,
                    is_active=True
                )
            )
            await trans.commit()
            await trans.close()
            return redirect('/links/me', status=302)

    except Exception:
        await trans.close()
        return json({'message': 'Creating new link failed'}, status=500)


@form_blueprint.route('/edit/<link_id>', methods=['GET'])
@login_required
@credential_whitelist_check
async def update_link_form(request, user, link_id):
    form = UpdateForm(request)
    try:
        async with request.app.engine.acquire() as conn:
            try:
                query = await conn.execute(
                    links.select().where(
                        links.columns['id'] == link_id
                    )
                )
                link = await query.fetchone()
                if not link:
                    raise Exception

                return html(template_loader(
                                template_file='edit_form.html',
                                form=form,
                                link=link,
                            ), status=200)

            except Exception:
                return json({'message': 'Link does not exist'}, status=404)

    except Exception:
        return json({'message': 'Getting update form failed'}, status=500)


@form_blueprint.route('/edit/<link_id>', methods=['POST'])
@login_required
@credential_whitelist_check
async def update_link_save(request, user, link_id):
    form = UpdateForm(request)
    if not form.validate():
        return json({'message': 'Form invalid'}, status=400)

    try:
        async with request.app.engine.acquire() as conn:
            trans = await conn.begin()
            link_update = links.update().where(links.columns['id'] == link_id)
            try:
                link_query = await conn.execute(links.select().where(
                    links.columns['id'] == link_id
                ))
                link_data = await link_query.fetchone()
                if not link_data:
                    raise Exception

            except Exception:
                await trans.close()
                return json({'message': 'Link does not exist'}, status=404)

            if form.password.data:
                fresh_salt = os.urandom(32)
                password = hashlib.pbkdf2_hmac(
                    'sha256',
                    form.password.data.encode('utf-8'),
                    fresh_salt,
                    100000
                )
                if link_data.password:
                    await conn.execute(salts.update().where(
                        salts.columns['identifier'] == link_data.identifier
                    ).values(salt=fresh_salt))
                else:
                    await conn.execute(salts.insert().values(
                            identifier=link_data.identifier,
                            salt=fresh_salt
                    ))

                await conn.execute(link_update.values(
                    url=form.url.data,
                    switch_date=form.switch_date.data,
                    password=password
                ))

            else:
                await conn.execute(link_update.values(
                    url=form.url.data,
                    switch_date=form.switch_date.data
                ))

            await trans.commit()
            await trans.close()
            return redirect('/links/me', status=302)

    except Exception:
        await trans.close()
        return json({'message': 'Editing link failed'}, status=500)
