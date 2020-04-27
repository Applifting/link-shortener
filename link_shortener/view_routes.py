'''
Copyright (C) 2020 Link Shortener Authors (see AUTHORS in Documentation).
Licensed under the MIT (Expat) License (see LICENSE in Documentation).
'''
from decouple import config

from sanic import Blueprint
from sanic.response import html, json, redirect

from sanic_oauth.blueprint import login_required

from sqlalchemy.sql.expression import select as sql_select

from link_shortener.models import actives, inactives
from link_shortener.templates import template_loader

from link_shortener.core.decorators import credential_whitelist_check


view_blueprint = Blueprint('views')


@view_blueprint.route('/<link_endpoint>', methods=['GET'])
async def redirect_link(request, link_endpoint):
    try:
        async with request.app.engine.acquire() as conn:
            query = await conn.execute(
                actives.select().where(
                    actives.columns['endpoint'] == link_endpoint
                )
            )
            link_data = await query.fetchone()
            return redirect(link_data.url)

    except Exception:
        return json({'message': 'link inactive or does not exist'}, status=400)


@view_blueprint.route('/', methods=['GET'])
async def landing_page(request):
    return redirect('/links/about')


@view_blueprint.route('/links/about', methods=['GET'])
async def about_page(request):
    try:
        return html(template_loader(template_file='about.html'), status=200)

    except Exception:
        return json({'message': 'getting route failed'}, status=500)


@view_blueprint.route('/links/all', methods=['GET'])
@login_required
@credential_whitelist_check()
async def all_active_links(request, user):
    try:
        async with request.app.engine.acquire() as conn:
            queryset = await conn.execute(actives.select())
            data = await queryset.fetchall()
            return html(template_loader(
                            template_file='all_links.html',
                            domain_name=config('DOMAIN_NAME'),
                            data=data
                        ), status=200)

    except Exception:
        return json({'message': 'getting links failed'}, status=500)


@view_blueprint.route('/links/me', methods=['GET'])
@login_required
@credential_whitelist_check()
async def owner_specific_links(request, user):
    try:
        async with request.app.engine.acquire() as conn:
            ac_queryset = await conn.execute(
                actives.select().where(
                    actives.columns['owner_id'] == user.id
                )
            )
            in_queryset = await conn.execute(
                inactives.select().where(
                    inactives.columns['owner_id'] == user.id
                )
            )
            ac_data = await ac_queryset.fetchall()
            in_data = await in_queryset.fetchall()
            return html(template_loader(
                            template_file='my_links.html',
                            domain_name=config('DOMAIN_NAME'),
                            ac_data=ac_data,
                            in_data=in_data
                        ), status=200)

    except Exception:
        return json({'message': 'getting your links failed'}, status=500)


@view_blueprint.route('/delete/<status>/<link_id>', methods=['GET'])
@login_required
@credential_whitelist_check()
async def delete_link(request, user, status, link_id):
    if (status == 'active'):
        table = actives
    elif (status == 'inactive'):
        table = inactives
    else:
        return json({'message': 'Path does not exist'}, status=400)

    try:
        async with request.app.engine.acquire() as conn:
            trans = await conn.begin()
            await conn.execute(
                table.delete().where(
                    table.columns['id'] == link_id
                )
            )
            await trans.commit()
            await trans.close()
            return redirect('/links/me')

    except Exception:
        await trans.close()
        return json({'message': 'deleting link failed'}, status=500)


@view_blueprint.route('/activate/<link_id>', methods=['GET'])
@login_required
@credential_whitelist_check()
async def activate_link(request, user, link_id):
    try:
        async with request.app.engine.acquire() as conn:
            trans = await conn.begin()
            await conn.execute(
                actives.insert().from_select(
                    [
                        'identifier',
                        'owner',
                        'owner_id',
                        'endpoint',
                        'url'
                    ],
                    sql_select([
                        inactives.c.identifier,
                        inactives.c.owner,
                        inactives.c.owner_id,
                        inactives.c.endpoint,
                        inactives.c.url
                    ]).where(inactives.c.id == link_id)
                )
            )
            await conn.execute(
                inactives.delete().where(
                    inactives.columns['id'] == link_id
                )
            )
            await trans.commit()
            await trans.close()
            return redirect('/links/me')

    except Exception:
        await trans.close()
        return json({'message': 'activating link failed'}, status=500)


@view_blueprint.route('/deactivate/<link_id>', methods=['GET'])
@login_required
@credential_whitelist_check()
async def deactivate_link(request, user, link_id):
    try:
        async with request.app.engine.acquire() as conn:
            trans = await conn.begin()
            await conn.execute(
                inactives.insert().from_select(
                    [
                        'identifier',
                        'owner',
                        'owner_id',
                        'endpoint',
                        'url'
                    ],
                    sql_select([
                        actives.c.identifier,
                        actives.c.owner,
                        actives.c.owner_id,
                        actives.c.endpoint,
                        actives.c.url
                    ]).where(actives.c.id == link_id)
                )
            )
            await conn.execute(
                actives.delete().where(
                    actives.columns['id'] == link_id
                )
            )
            await trans.commit()
            await trans.close()
            return redirect('/links/me')

    except Exception as error:
        print(error)
        await trans.close()
        return json({'message': 'deactivating link failed'}, status=500)
