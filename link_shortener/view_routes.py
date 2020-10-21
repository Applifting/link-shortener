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
from link_shortener.commands.switch import activate_link, deactivate_link
from link_shortener.commands.delete import delete_link
from link_shortener.commands.redirect import redirect_link
from link_shortener.core.exceptions import (DuplicateActiveLinkForbidden,
                                            NotFoundException)
from link_shortener.core.decorators import credential_whitelist_check
from link_shortener.core.filter import filter_links, get_filter_dict


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


@view_blueprint.route('/status/liveness')
def liveness_check(request):
    return text('OK')


@view_blueprint.route('/<link_endpoint>', methods=['GET'])
async def redirect_link_view(request, link_endpoint):
    try:
        target = await redirect_link(request, link_endpoint)
        if (target[:10] == '/authorize/'):
            return redirect(target)

        return html(template_loader(
                        template_file='redirect.html',
                        link=target,
                    ), status=307)
    except NotFoundException:
        return html(template_loader('message.html'), status=404)


@view_blueprint.route('/', methods=['GET'])
async def landing_page(request):
    return redirect('/links/all', status=301)


@view_blueprint.route('/links/all', methods=['GET'])
@login_required
@credential_whitelist_check
async def all_active_links(request, user):
    filters = get_filter_dict(request)
    link_data = await retrieve_links(
        request,
        {'is_active': filters['is_active']}
    )
    filtered_data = filter_links(link_data, filters)
    return html(template_loader(
                    template_file='all_links.html',
                    domain_name=config('DOMAIN_NAME'),
                    data=filtered_data
                ), status=200)


@view_blueprint.route('/delete/<link_id>', methods=['GET'])
@login_required
@credential_whitelist_check
async def delete_link_view(request, user, link_id):
    try:
        await delete_link(request, link_id)
        return redirect('/links/all?origin=delete&status=deleted')
    except NotFoundException:
        return html(template_loader('message.html'), status=404)


@view_blueprint.route('/delete/<link_id>/confirm', methods=['GET'])
@login_required
@credential_whitelist_check
async def confirm_delete_link_view(request, user, link_id):
    return html(template_loader(
                    template_file='delete.html',
                    link_id=link_id), status=200)


@view_blueprint.route('/activate/<link_id>', methods=['GET'])
@login_required
@credential_whitelist_check
async def activate_link_view(request, user, link_id):
    try:
        await activate_link(request, link_id)
        message = 'activated'  # status = 200
    except NotFoundException:
        return html(template_loader('message.html'), status=404)
    except DuplicateActiveLinkForbidden:
        message = 'duplicate'  # status = 409

    params = f'?origin=activate&status={message}'
    return redirect(f'/edit/{link_id}{params}')


@view_blueprint.route('/deactivate/<link_id>', methods=['GET'])
@login_required
@credential_whitelist_check
async def deactivate_link_view(request, user, link_id):
    try:
        await deactivate_link(request, link_id)
        params = '?origin=deactivate&status=deactivated'
        return redirect(f'/edit/{link_id}{params}')
    except NotFoundException:
        return html(template_loader('message.html'), status=404)
