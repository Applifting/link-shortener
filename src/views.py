'''
Copyright (C) 2020 Link Shortener Authors (see AUTHORS in Documentation).
Licensed under the MIT (Expat) License (see LICENSE in Documentation).
'''
from sanic import Blueprint
from sanic.response import html, json

from sanic_oauth.blueprint import login_required

from commands import template_generators
from initialise_db import initdb_blueprint


view_blueprint = Blueprint('views')

actives = initdb_blueprint.active_table
inactives = initdb_blueprint.inactive_table


@view_blueprint.route('/links/all', methods=['GET'])
async def all_active_links(request):
    try:
        async with request.app.engine.acquire() as conn:
            data = []
            queryset = await conn.execute(actives.select())
            for row in await queryset.fetchall():
                data.append((row.id, row.endpoint, row.owner, row.url))

            return html(
                template_generators.all_links_page_generator(data),
                status=200
            )

    except Exception as error:
        print(error)
        return json({'message': 'getting links failed'}, status=500)


@view_blueprint.route('/links/me', methods=['GET'])
@login_required
async def owner_specific_links(request, user):
    try:
        async with request.app.engine.acquire() as conn:
            ac_data, in_data = [], []
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
            for row in await ac_queryset.fetchall():
                ac_data.append((row.id, row.endpoint, row.url))

            for row in await in_queryset.fetchall():
                in_data.append((row.id, row.endpoint, row.url))

            return html(
                template_generators.my_links_page_generator(ac_data, in_data),
                status=200
            )

    except Exception as error:
        print(error)
        return json({'message': 'getting your links failed'}, status=500)


@view_blueprint.route('/delete/active/<link_id>', methods=['GET'])
@login_required
async def delete_active_link(request, user, link_id):
    try:
        async with request.app.engine.acquire() as conn:
            trans = await conn.begin()
            await conn.execute(
                'DELETE FROM active_links WHERE id = %s',
                link_id
            )
            await trans.commit()
            await trans.close()
            return redirect('/links/me')

    except Exception as error:
        return json({'message': 'deleting link failed'})
