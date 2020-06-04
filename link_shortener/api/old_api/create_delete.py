'''
Copyright (C) 2020 Link Shortener Authors (see AUTHORS in Documentation).
Licensed under the MIT (Expat) License (see LICENSE in Documentation).
'''
from datetime import date
from decouple import config
from json import loads

from sanic import Blueprint
from sanic.response import json

from link_shortener.models import links, salts

from link_shortener.commands.create import create_link


api_create_delete_blueprint = Blueprint('create_delete')


@api_create_delete_blueprint.route('/api/links', methods=['POST'])
async def api_create_link(request):
    try:
        token = request.headers['Bearer']
        if (token != config('ACCESS_TOKEN')):
            return json({'message': 'Unauthorized'}, status=401)

    except KeyError:
        return json({'message': 'Please provide a token'}, status=400)

    try:
        data = {}
        payload = loads(request.body)

        data['owner'] = payload['owner']
        data['owner_id'] = payload['owner_id']
        data['endpoint'] = payload['endpoint']
        data['url'] = payload['url']

        sd = payload['switch_date']
        data['switch_date'] = date(sd['Year'], sd['Month'], sd['Day'])

        print(data)
        message, status = await create_link(request, data)
        return json({'message': message}, status=status)

    except KeyError:
        return json({'message': 'Please provide all data'}, status=400)

    except Exception:
        return json({'message': 'Bad request and/or payload'}, status=400)

    try:
        async with request.app.engine.acquire() as conn:
            trans = await conn.begin()
            identifier = str(uuid.uuid1())
            try:
                await conn.execute(
                    actives.insert().values(
                        identifier=identifier,
                        owner=owner,
                        owner_id=owner_id,
                        endpoint=endpoint,
                        url=url,
                        switch_date=switch_date
                    )
                )
                await trans.commit()
                await trans.close()
                return json({'message': 'Link created'}, status=201)

            except Exception:
                await trans.close()
                return json({'message': 'Endpoint already exists'}, status=409)

    except Exception:
        await trans.close()
        return json({'message': 'Creating link failed'}, status=500)


@api_create_delete_blueprint.route(
    '/api/link/<status>/<link_id>',
    methods=['DELETE']
)
async def api_delete_link_by_id(request, status, link_id):
    try:
        token = request.headers['Bearer']
        if (token != config('ACCESS_TOKEN')):
            return json({'message': 'Unauthorized'}, status=401)

    except KeyError:
        return json({'message': 'Please provide a token'}, status=400)

    if (status == 'active'):
        table = actives
    elif (status == 'inactive'):
        table = inactives
    else:
        return json(
            {'message': 'Status "{}" does not exist'.format(status)},
            status=400
        )

    try:
        async with request.app.engine.acquire() as conn:
            trans = await conn.begin()
            query = await conn.execute(
                table.select().where(
                    table.columns['id'] == link_id
                )
            )
            try:
                link_data = await query.fetchone()
                if link_data:
                    await conn.execute(
                        table.delete().where(
                            table.columns['id'] == link_id
                        )
                    )
                    await trans.commit()
                    await trans.close()
                    return json({}, status=204)

                await trans.close()
                return json({'message': 'Link does not exist'}, status=404)

            except Exception:
                trans.close()
                return json({'message': 'Link does not exist'}, status=404)

    except Exception:
        await trans.close()
        return json({'message': 'Deleting link failed'}, status=500)


@api_create_delete_blueprint.route(
    '/api/link/<identifier>',
    methods=['DELETE']
)
async def api_delete_link_by_identifier(request, identifier):
    try:
        token = request.headers['Bearer']
        if (token != config('ACCESS_TOKEN')):
            return json({'message': 'Unauthorized'}, status=401)

    except KeyError:
        return json({'message': 'Please provide a token'}, status=400)

    try:
        async with request.app.engine.acquire() as conn:
            trans = await conn.begin()
            ac_queryset = await conn.execute(
                actives.select().where(
                    actives.columns['identifier'] == identifier
                )
            )
            link_data = await ac_queryset.fetchone()
            table = actives
            if not link_data:
                in_queryset = await conn.execute(
                    inactives.select().where(
                        inactives.columns['identifier'] == identifier
                    )
                )
                link_data = await in_queryset.fetchone()
                table = inactives
                if not link_data:
                    await trans.close()
                    return json({'message': 'Link does not exist'}, status=404)

            await conn.execute(
                table.delete().where(
                    table.columns['identifier'] == link_data.identifier
                )
            )
            await trans.commit()
            await trans.close()
            return json({}, status=204)

    except Exception:
        await trans.close()
        return json({'message': 'Deleting link failed'}, status=500)
