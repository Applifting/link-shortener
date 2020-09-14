'''
Copyright (C) 2020 Link Shortener Authors (see AUTHORS in Documentation).
Licensed under the MIT (Expat) License (see LICENSE in Documentation).
'''
from decouple import config

from sanic import Blueprint
from sanic.response import html, redirect, text, json

from sanic_oauth.blueprint import login_required

from prometheus_client import Counter, generate_latest

from link_shortener.templates import template_loader

from link_shortener.commands.retrieve import retrieve_links
from link_shortener.commands.update import reset_password
from link_shortener.commands.switch import activate_link, deactivate_link
from link_shortener.commands.delete import delete_link
from link_shortener.commands.redirect import redirect_link
from link_shortener.commands.filter import filter_links

from link_shortener.core.exceptions import (DuplicateActiveLinkForbidden,
                                            NotFoundException)
from link_shortener.core.decorators import credential_whitelist_check


view_blueprint = Blueprint('views')
redirect_counter = Counter(
    'redirect_count',
    'Number of successful link redirections',
    ['link_id', 'referer']
)


@view_blueprint.route('/metrics', methods=['GET'])
async def requests_count(request):
    try:
        count = generate_latest(redirect_counter)
        return text(count.decode())
    except Exception as error:
        return json({'message': error}, status=500)


@view_blueprint.route('/<link_endpoint>', methods=['GET'])
async def redirect_link_view(request, link_endpoint):
    try:
        target = await redirect_link(request, link_endpoint)
        return redirect(target, status=307)
    except NotFoundException:
        return html(template_loader(
                        template_file='message.html',
                        payload='Link inactive or does not exist',
                        status_code='404'
                    ), status=404)


@view_blueprint.route('/', methods=['GET'])
async def landing_page(request):
    return redirect('/links/all', status=301)


@view_blueprint.route('/links/all', methods=['GET'])
@login_required
@credential_whitelist_check
async def all_active_links(request, user):
    filter_set = {'is_active', 'owner', 'search'}
    filters = {element: request.args.get(element) for element in filter_set}

    if filters['is_active'] is None:
        filters['is_active'] = True

    data_db = await retrieve_links(request, {'is_active': filters['is_active']})
    link_data = await filter_links(data_db, filters)
    
    return html(template_loader(
                    template_file='all_links.html',
                    domain_name=config('DOMAIN_NAME'),
                    data=link_data,
                ), status=200)


@view_blueprint.route('/links/me', methods=['GET'])
@login_required
@credential_whitelist_check
async def owner_specific_links(request, user):
    link_data = await retrieve_links(request, filters={'owner_id': user.id})
    return html(template_loader(
                    template_file='my_links.html',
                    domain_name=config('DOMAIN_NAME'),
                    link_data=link_data
                ), status=200)


@view_blueprint.route('/delete/<link_id>', methods=['GET'])
@login_required
@credential_whitelist_check
async def delete_link_view(request, user, link_id):
    try:
        await delete_link(request, link_id)
        status = 200
    except NotFoundException:
        status = 404
    finally:
        params = f'?from=delete&status={status}'
        return redirect(f'/links/all{params}')


@view_blueprint.route('/delete/<link_id>/confirm', methods=['GET'])
@login_required
@credential_whitelist_check
async def confirm_delete_link_view(request, user, link_id):
    return html(template_loader(
                    template_file='delete_link.html',
                    link_id=link_id), status=200)


@view_blueprint.route('/activate/<link_id>', methods=['GET'])
@login_required
@credential_whitelist_check
async def activate_link_view(request, user, link_id):
    try:
        await activate_link(request, link_id)
        status = 200
    except NotFoundException:
        status = 404
    except DuplicateActiveLinkForbidden:
        status = 400
    finally:
        params = f'?from=activate&status={status}'
        return redirect(f'/edit/{link_id}{params}')


@view_blueprint.route('/deactivate/<link_id>', methods=['GET'])
@login_required
@credential_whitelist_check
async def deactivate_link_view(request, user, link_id):
    try:
        await deactivate_link(request, link_id)
        status = 200
    except NotFoundException:
        status = 404
    finally:
        params = f'?from=deactivate&status={status}'
        return redirect(f'/edit/{link_id}{params}')


@view_blueprint.route('/reset/<link_id>', methods=['GET'])
@login_required
@credential_whitelist_check
async def reset_password_view(request, user, link_id):
    try:
        await reset_password(request, link_id)
        status = 200
    except NotFoundException:
        status = 404
    finally:
        params = f'?from=reset&status={status}'
        return redirect(f'/edit/{link_id}{params}')
