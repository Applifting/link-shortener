'''
Copyright (C) 2020 Link Shortener Authors (see AUTHORS in Documentation).
Licensed under the MIT (Expat) License (see LICENSE in Documentation).
'''
from sanic import Blueprint
from sanic.response import redirect, html

from sanic_oauth.blueprint import login_required

from sanic_wtf import SanicForm

from wtforms import StringField, SubmitField, PasswordField, DateField
from wtforms.validators import DataRequired

from link_shortener.templates import template_loader

from link_shortener.commands.authorize import check_auth_form, check_password
from link_shortener.commands.update import check_update_form, update_link
from link_shortener.commands.create import create_link

from link_shortener.core.decorators import credential_whitelist_check
from link_shortener.core.exceptions import (AccessDeniedException,
                                            DuplicateActiveLinkForbidden,
                                            FormInvalidException,
                                            NotFoundException)


form_blueprint = Blueprint('forms')


class CreateForm(SanicForm):
    endpoint = StringField('Endpoint', validators=[DataRequired()])
    url = StringField('URL', validators=[DataRequired()])
    password = StringField('Password')
    switch_date = DateField('Status switch date')
    submit = SubmitField('Create')


class UpdateForm(SanicForm):
    url = StringField('URL', validators=[])
    password = StringField('Password', validators=[])
    switch_date = DateField('Status switch date')
    submit = SubmitField('Update')


class PasswordForm(SanicForm):
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')


@form_blueprint.route('/authorize/<link_id>', methods=['GET'])
async def link_password_form(request, link_id):
    try:
        form = PasswordForm(request)
        data = await check_auth_form(request, link_id)
        return html(template_loader(
                        template_file='password_form.html',
                        form=form,
                        payload=data,
                        status_code='200'
                    ), status=200)
    except NotFoundException:
        params = '?from=authorize&status=404'
        return redirect(f'/links/all{params}')


@form_blueprint.route('/authorize/<link_id>', methods=['POST'])
async def link_password_save(request, link_id):
    try:
        form = PasswordForm(request)
        link = await check_password(request, link_id, form)
        return redirect(link, status=307)
    except FormInvalidException:
        status = 400
    except NotFoundException:
        status = 404
    except AccessDeniedException:
        status = 401

    params = f'?from=authorize&status={status}'
    return redirect(f'/authorize/{link_id}/{params}')


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
    headers = {}
    try:
        form = CreateForm(request)
        if not form.validate():
            raise FormInvalidException

        form_data = {
            'owner': user.email,
            'owner_id': user.id,
            'password': form.password.data,
            'endpoint': form.endpoint.data,
            'url': form.url.data,
            'switch_date': form.switch_date.data
        }
        await create_link(request, data=form_data)
        status = 201
    except FormInvalidException:
        status = 400
    except DuplicateActiveLinkForbidden:
        status = 409
    finally:
        params = f'?from=create&status={status}'
        return redirect(f'/links/all/{params}')


@form_blueprint.route('/edit/<link_id>', methods=['GET'])
@login_required
@credential_whitelist_check
async def update_link_form(request, user, link_id):
    try:
        message = request.args if request.args else None
        form = UpdateForm(request)
        data = await check_update_form(request, link_id)
        return html(template_loader(
                        template_file='edit_form.html',
                        form=form,
                        payload=data,
                        message=message,
                        status_code='200'
                    ), status=200)
    except NotFoundException:
        params = f'?from=edit&status=404'
        return redirect(f'/links/all{params}')


@form_blueprint.route('/edit/<link_id>', methods=['POST'])
@login_required
@credential_whitelist_check
async def update_link_save(request, user, link_id):
    try:
        form = UpdateForm(request)
        if not form.validate():
            raise FormInvalidException

        form_data = {
            'password': form.password.data,
            'url': form.url.data,
            'switch_date': form.switch_date.data
        }
        await update_link(request, link_id=link_id, data=form_data)
        status = 200
    except FormInvalidException:
        status = 400
    except NotFoundException:
        status = 404
    finally:
        params = f'?from=edit&status={status}'
        return redirect(f'/links/all{params}')
