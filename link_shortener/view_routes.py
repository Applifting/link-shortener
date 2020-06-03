'''
Copyright (C) 2020 Link Shortener Authors (see AUTHORS in Documentation).
Licensed under the MIT (Expat) License (see LICENSE in Documentation).
'''
from decouple import config

from sanic import Blueprint
from sanic.response import html, redirect

from sanic_oauth.blueprint import login_required

from link_shortener.models import links
from link_shortener.templates import template_loader

from link_shortener.commands.retrieve import retrieve_links
from link_shortener.commands.update import reset_password
from link_shortener.commands.switch import activate_link, deactivate_link
from link_shortener.commands.delete import delete_link

from link_shortener.core.decorators import credential_whitelist_check


view_blueprint = Blueprint('views')


@view_blueprint.route('/<link_endpoint>', methods=['GET'])
async def redirect_link(request, link_endpoint):
    try:
        async with request.app.engine.acquire() as conn:
            try:
                query = await conn.execute(
                    links.select().where(
                        links.columns['endpoint'] == link_endpoint
                    ).where(
                        links.columns['is_active'] == True
                    )
                )
                link_data = await query.fetchone()
                if not link_data:
                    raise Exception

                if not link_data.password:
                    return redirect(link_data.url, status=301)

                return redirect(
                    '/authorize/{}'.format(link_data.id),
                    status=301
                )

            except Exception:
                return html(template_loader(
                                template_file='message.html',
                                payload='Link inactive or does not exist',
                                status_code='404'
                            ), status=404)

    except Exception:
        return html(template_loader(
                        template_file='message.html',
                        payload='Server error',
                        status_code='500'
                    ), status=500)


@view_blueprint.route('/', methods=['GET'])
async def landing_page(request):
    return redirect('/links/about', status=301)


@view_blueprint.route('/links/about', methods=['GET'])
async def about_page(request):
    try:
        return html(template_loader(template_file='about.html'), status=200)

    except Exception:
        return html(template_loader(
                        template_file='message.html',
                        payload='Template failed loading',
                        status_code='500'
                    ), status=500)


@view_blueprint.route('/links/all', methods=['GET'])
@login_required
@credential_whitelist_check
async def all_active_links(request, user):
    try:
        link_data = await retrieve_links(request, {'is_active': True})
        return html(template_loader(
                        template_file='all_links.html',
                        domain_name=config('DOMAIN_NAME'),
                        data=link_data
                    ), status=200)

    except Exception:
        return html(template_loader(
                        template_file='message.html',
                        payload='Template failed loading',
                        status_code='500'
                    ), status=500)


@view_blueprint.route('/links/me', methods=['GET'])
@login_required
@credential_whitelist_check
async def owner_specific_links(request, user):
    try:
        link_data = await retrieve_links(request, {'owner_id': user.id})
        return html(template_loader(
                        template_file='my_links.html',
                        domain_name=config('DOMAIN_NAME'),
                        link_data=link_data
                    ), status=200)

    except Exception:
        return html(template_loader(
                        template_file='message.html',
                        payload='Template failed loading',
                        status_code='500'
                    ), status=500)


@view_blueprint.route('/delete/<link_id>', methods=['GET'])
@login_required
@credential_whitelist_check
async def delete_link_view(request, user, link_id):
    message, status_code = await delete_link(request, link_id)
    return html(template_loader(
                    template_file='message.html',
                    payload=message,
                    status_code=str(status_code)
                ), status=status_code)


@view_blueprint.route('/activate/<link_id>', methods=['GET'])
@login_required
@credential_whitelist_check
async def activate_link_view(request, user, link_id):
    message, status_code = await activate_link(request, link_id)
    return html(template_loader(
                    template_file='message.html',
                    payload=message,
                    status_code=str(status_code)
                ), status=status_code)


@view_blueprint.route('/deactivate/<link_id>', methods=['GET'])
@login_required
@credential_whitelist_check
async def deactivate_link_view(request, user, link_id):
    message, status_code = await deactivate_link(request, link_id)
    return html(template_loader(
                    template_file='message.html',
                    payload=message,
                    status_code=str(status_code)
                ), status=status_code)


@view_blueprint.route('/reset/<link_id>', methods=['GET'])
@login_required
@credential_whitelist_check
async def reset_password_view(request, user, link_id):
    message, status_code = await reset_password(request, link_id)
    return html(template_loader(
                    template_file='message.html',
                    payload=message,
                    status_code=str(status_code)
                ), status=status_code)
