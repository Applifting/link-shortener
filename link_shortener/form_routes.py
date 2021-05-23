'''
Copyright (C) 2020 Link Shortener Authors (see AUTHORS in Documentation).
Licensed under the MIT (Expat) License (see LICENSE in Documentation).
'''
from decouple import config
from sanic import Blueprint
from sanic.response import html, redirect

from sanic_oauth.blueprint import login_required

from sanic_wtf import SanicForm

from wtforms import StringField, SubmitField, PasswordField, DateField
from wtforms.validators import DataRequired, NoneOf

from link_shortener.templates import template_loader

from link_shortener.commands.authorize import check_auth_form, check_password
from link_shortener.commands.update import check_update_form, update_link
from link_shortener.commands.create import create_link
from link_shortener.commands.retrieve import retrieve_links
from link_shortener.core.decorators import credential_whitelist_check
from link_shortener.core.exceptions import (AccessDeniedException,
                                            DuplicateActiveLinkForbidden,
                                            FormInvalidException,
                                            LinkNotAllowed,
                                            NotFoundException)
from link_shortener.core.filter import filter_links, get_filter_dict
from link_shortener.core.generics import generate_random_suffix


form_blueprint = Blueprint('forms')


class QuickCreateForm(SanicForm):
    url = StringField('URL', validators=[DataRequired()], id= 'input_shortlink')
    submit = SubmitField('Create')


class UpdateForm(SanicForm):
    endpoint = StringField(
        'Endpoint',
        validators=[DataRequired(), NoneOf('/')]
    )
    url = StringField('URL', validators=[DataRequired()])
    password = StringField('Password', validators=[])
    switch_date = DateField('Status switch date')
    submit = SubmitField('Update')


class PasswordForm(SanicForm):
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Visit shortlink')


@form_blueprint.route('/authorize/<link_id>', methods=['GET'])
async def link_password_form(request, link_id):
    try:
        form = PasswordForm(request)
        data = await check_auth_form(request, link_id)
        return html(template_loader(
                        template_file='password_form.html',
                        form=form,
                        payload=data
                    ), status=200)
    except NotFoundException:
        return html(template_loader('message.html'), status=404)


@form_blueprint.route('/authorize/<link_id>', methods=['POST'])
async def link_password_save(request, link_id):
    try:
        form = PasswordForm(request)
        link = await check_password(request, link_id, form)
        return html(template_loader(
                        template_file='redirect.html',
                        link=link,
                    ), status=307)
    except FormInvalidException:
        message = 'invalid-form'  # status = 400
    except NotFoundException:
        return html(template_loader('message.html'), status=404)
    except AccessDeniedException:
        message = 'incorrect-password'  # status = 401

    params = f'?origin=authorize&status={message}'
    return redirect(f'/authorize/{link_id}{params}')


@form_blueprint.route('/links/all', methods=['GET'])
@login_required
@credential_whitelist_check
async def link_list_form(request, user):
    form = QuickCreateForm(request)
    filters = get_filter_dict(request)
    link_data = await retrieve_links(
        request,
        {'is_active': filters['is_active']}
    )
    filtered_data = filter_links(link_data, filters)
    return html(template_loader(
                    template_file='all_links.html',
                    form=form,
                    domain_name=config('DOMAIN_NAME'),
                    data=filtered_data
                ), status=200)


@form_blueprint.route('/links/all', methods=['POST'])
@login_required
@credential_whitelist_check
async def quick_create_form(request, user):
    try:
        form = QuickCreateForm(request)
        if not form.validate():
            raise FormInvalidException

        endpoint = generate_random_suffix(6)
        form_data = {
            'owner': user.email,
            'owner_id': user.id,
            'password': None,
            'endpoint': endpoint,
            'url': form.url.data,
            'switch_date': None
        }
        await create_link(request, data=form_data)
        message = 'created'  # status = 201
    except FormInvalidException:
        message = 'invalid-form'  # status = 400
    except DuplicateActiveLinkForbidden:
        message = 'duplicate'  # status = 409
    except LinkNotAllowed:
        message = 'not-allowed'  # status = 400
    finally:
        params = f'?origin=create&status={message}&created={endpoint}'
        return redirect(f'/links/all{params}')


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
                        default_password=config('DEFAULT_PASSWORD')
                    ), status=200)
    except NotFoundException:
        return html(template_loader('message.html'), status=404)


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
            'endpoint': form.endpoint.data,
            'url': form.url.data,
            'switch_date': form.switch_date.data
        }
        await update_link(request, link_id=link_id, data=form_data)
        message = 'updated'   # status = 200
    except FormInvalidException:
        message = 'form-invalid'  # status = 400
    except LinkNotAllowed:
        message = 'not-allowed'  # status = 400
    except NotFoundException:
        return html(template_loader('message.html'), status=404)
    except DuplicateActiveLinkForbidden:
        message = 'duplicate'  # status = 409

    return redirect(f'/links/all?origin=edit&status={message}')
