'''
Copyright (C) 2020 Link Shortener Authors (see AUTHORS in Documentation).
Licensed under the MIT (Expat) License (see LICENSE in Documentation).
'''
from decouple import config

from sanic import Blueprint
from sanic.response import html, json, redirect

from sanic_oauth.blueprint import login_required

from sqlalchemy.sql.expression import select as sql_select

from link_shortener.models import links, salts
from link_shortener.templates import template_loader

from link_shortener.commands.retrieve import retrieve_links
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

                if link_data.password is None:
                    return redirect(link_data.url, status=301)

                return redirect(
                    '/authorize/{}'.format(link_data.id),
                    status=301
                )

            except Exception:
                return json(
                    {'message': 'Link inactive or does not exist'},
                    status=404
                )

    except Exception:
        return json({'message': 'Server error'}, status=500)


@view_blueprint.route('/', methods=['GET'])
async def landing_page(request):
    return redirect('/links/about', status=301)


@view_blueprint.route('/links/about', methods=['GET'])
async def about_page(request):
    try:
        return html(template_loader(template_file='about.html'), status=200)

    except Exception:
        return json({'message': 'Template failed loading'}, status=500)


@view_blueprint.route('/links/all', methods=['GET'])
@login_required
@credential_whitelist_check
async def all_active_links(request, user):
    # try:
    #     async with request.app.engine.acquire() as conn:
    #         queryset = await conn.execute(links.select())
    #         data = await queryset.fetchall()
    #         return html(template_loader(
    #                         template_file='all_links.html',
    #                         domain_name=config('DOMAIN_NAME'),
    #                         data=data
    #                     ), status=200)
    #
    try:
        link_data = await retrieve_links(request, {'is_active': True})
        return html(template_loader(
                        template_file='all_links.html',
                        domain_name=config('DOMAIN_NAME'),
                        data=link_data
                    ), status=200)

    except Exception:
        return json({'message': 'Template failed loading'}, status=500)


@view_blueprint.route('/links/me', methods=['GET'])
@login_required
@credential_whitelist_check
async def owner_specific_links(request, user):
    # try:
    #     async with request.app.engine.acquire() as conn:
    #         queryset = await conn.execute(
    #             links.select().where(
    #                 links.columns['owner_id'] == user.id
    #             )
    #         )
    #         link_data = await queryset.fetchall()
    #         return html(template_loader(
    #                         template_file='my_links.html',
    #                         domain_name=config('DOMAIN_NAME'),
    #                         link_data=link_data
    #                     ), status=200)
    try:
        link_data = await retrieve_links(request, {'owner_id': user.id})
        return html(template_loader(
                        template_file='my_links.html',
                        domain_name=config('DOMAIN_NAME'),
                        link_data=link_data
                    ), status=200)

    except Exception:
        return json({'message': 'Template failed loading'}, status=500)


@view_blueprint.route('/delete/<link_id>', methods=['GET'])
@login_required
@credential_whitelist_check
async def delete_link_view(request, user, link_id):
    message, status_code = await delete_link(request, link_id)
    return html(template_loader(
                    template_file='message.html',
                    message=message,
                    status_code=str(status_code)
                ), status=status_code)
    # try:
    #     async with request.app.engine.acquire() as conn:
    #         trans = await conn.begin()
    #         await conn.execute(
    #             links.delete().where(
    #                 links.columns['id'] == link_id
    #             )
    #         )
    #         await trans.commit()
    #         await trans.close()
    #         return redirect('/links/me', status=302)
    #
    # except Exception:
    #     await trans.close()
    #     return json({'message': 'Deleting failed'}, status=500)


@view_blueprint.route('/activate/<link_id>', methods=['GET'])
@login_required
@credential_whitelist_check
async def activate_link(request, user, link_id):
    try:
        async with request.app.engine.acquire() as conn:
            trans = await conn.begin()
            try:
                query = await conn.execute(
                    links.select().where(
                        links.columns['id'] == link_id
                    )
                )
                link_data = await query.fetchone()
                if not link_data:
                    await trans.close()
                    raise Exception

            except Exception:
                await trans.close()
                return json({'message': 'Link does not exist'}, status=404)

            try:
                endpoint_query = await conn.execute(
                    links.select().where(
                        links.columns['endpoint'] == link_data.endpoint
                    ).where(
                        links.columns['is_active'] == True
                    ).where(
                        links.columns['id'] != link_id
                    )
                )
                active_endpoint = await endpoint_query.fetchone()
                if not active_endpoint:
                    raise Exception

                await trans.close()
                return json(
                    {'message': 'That active endpoint already exists'},
                    status=400
                )

            except Exception:
                await conn.execute(
                    links.update().where(
                        links.columns['id'] == link_id
                    ).values(is_active=True)
                )
                await trans.commit()
                await trans.close()
                return redirect('/links/me', status=302)

    except Exception:
        await trans.close()
        return json({'message': 'Activating failed'}, status=500)


@view_blueprint.route('/deactivate/<link_id>', methods=['GET'])
@login_required
@credential_whitelist_check
async def deactivate_link(request, user, link_id):
    try:
        async with request.app.engine.acquire() as conn:
            trans = await conn.begin()
            try:
                query = await conn.execute(
                    links.select().where(
                        links.columns['id'] == link_id
                    )
                )
                link = await query.fetchone()
                if not link:
                    raise Exception

                await conn.execute(
                    links.update().where(
                        links.columns['id'] == link_id
                    ).values(is_active=False)
                )
                await trans.commit()
                await trans.close()
                return redirect('/links/me', status=302)

            except Exception:
                await trans.close()
                return json({'message': 'Link does not exist'}, status=404)

    except Exception:
        await trans.close()
        return json({'message': 'Deactivating failed'}, status=500)


@view_blueprint.route('/reset/<link_id>', methods=['GET'])
@login_required
@credential_whitelist_check
async def reset_password_view(request, user, link_id):
    try:
        async with request.app.engine.acquire() as conn:
            trans = await conn.begin()
            try:
                query = await conn.execute(
                    links.select().where(
                        links.columns['id'] == link_id
                    )
                )
                link_data = await query.fetchone()
                if not link_data:
                    await trans.close()
                    raise Exception

                await conn.execute(
                    links.update().where(
                        links.columns['id'] == link_id
                    ).values(
                        password=None
                    )
                )
                await conn.execute(
                    salts.delete().where(
                        salts.columns['identifier'] == link_data.identifier
                    )
                )
                await trans.commit()
                await trans.close()
                return redirect('/links/me', status=302)

            except Exception:
                await trans.close()
                return json({'message': 'Link does not exist'}, status=404)

    except Exception:
        await trans.close()
        return json({'message': 'Resetting password failed'}, status=500)
