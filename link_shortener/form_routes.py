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
        return html(template_loader(
                        template_file='message.html',
                        payload='Link has no password or does not exist',
                        status_code='404'
                    ), status=404)


@form_blueprint.route('/authorize/<link_id>', methods=['POST'])
async def link_password_save(request, link_id):
    try:
        form = PasswordForm(request)
        link = await check_password(request, link_id, form)
        return redirect(link, status=307)
    except FormInvalidException:
        status, message = 400, 'Form invalid'
    except NotFoundException:
        status, message = 404, 'Link has no password or does not exist'
    except AccessDeniedException:
        status, message = 401, 'Password incorrect'

    return html(template_loader(
                    template_file='message.html',
                    payload=message,
                    status_code=str(status)
                ), status=status)


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
    try:
        form = CreateForm(request)
        await create_link(request, data=form, user_data=user, from_api=False)
        status, message = 201, 'Link created successfully'
    except FormInvalidException:
        status, message = 400, 'Form invalid'
    except DuplicateActiveLinkForbidden:
        status, message = 409, 'An active link with that name already exists'
    finally:
        return html(template_loader(
                        template_file='message.html',
                        payload=message,
                        status_code=str(status)
                    ), status=status)


@form_blueprint.route('/edit/<link_id>', methods=['GET'])
@login_required
@credential_whitelist_check
async def update_link_form(request, user, link_id):
    try:
        form = UpdateForm(request)
        data = await check_update_form(request, link_id)
        return html(template_loader(
                        template_file='edit_form.html',
                        form=form,
                        payload=data,
                        status_code='200'
                    ), status=200)
    except NotFoundException:
        return html(template_loader(
                        template_file='message.html',
                        payload='Link does not exist',
                        status_code='404'
                    ), status=404)


@form_blueprint.route('/edit/<link_id>', methods=['POST'])
@login_required
@credential_whitelist_check
async def update_link_save(request, user, link_id):
    try:
        form = UpdateForm(request)
        await update_link(request, link_id, data=form, from_api=False)
        status, message = 200, 'Link updated successfully'
    except FormInvalidException:
        status, message = 400, 'Form invalid'
    except NotFoundException:
        status, message = 404, 'Link does not exist'
    finally:
        return html(template_loader(
                        template_file='message.html',
                        payload=message,
                        status_code=str(status)
                    ), status=status)
