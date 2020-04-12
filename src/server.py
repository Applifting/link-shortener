'''
Copyright (C) 2020 Link Shortener Authors
Licensed under the MIT (Expat) License. See the LICENSE file found in the
top-level directory of this distribution.
'''
from sanic import Sanic, response
from sanic.response import json

from json import dumps

from listeners import listener_blueprint


app = Sanic(__name__)
app.blueprint(listener_blueprint)

table = listener_blueprint.table


@app.route('/api/links', methods=['GET'])
async def get_links(request):
    try:
        async with app.engine.acquire() as conn:
            data = []
            queryset = await conn.execute(table.select())
            for row in await queryset.fetchall():
                data.append({
                    'endpoint': row.endpoint,
                    'url': row.url
                })
            return json(dumps(data), status=200)

    except Exception as error:
        print(error)
        return json({'message': 'getting links failed'}, status=500)


@app.route('/<link_endpoint>')
async def redirect_link(request, link_endpoint):
    try:
        async with app.engine.acquire() as conn:
            query = await conn.execute(
                table.select().where(
                    table.columns['endpoint'] == link_endpoint
                )
            )
            url = await query.fetchone()
            return response.redirect(url[1])

    except Exception as error:
        print(error)
        return json({'message': 'link does not exist'}, status=400)


if (__name__ == '__main__'):
    app.run(host='0.0.0.0', port=8000)
