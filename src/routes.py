'''
Copyright (C) 2020 Link Shortener Authors (see AUTHORS in Documentation).
Licensed under the MIT (Expat) License (see LICENSE in Documentation).
'''
from sanic import Blueprint
from sanic.response import html, json

from commands import template_generators


route_blueprint = Blueprint('routes')


# @route_blueprint.route('/', methods=['GET'])
# async def get_active_links(request):
#     try:
#         async with app.engine.acquire() as conn:
#             data = []
#             queryset = await conn.execute(actives.select())
#             for row in await queryset.fetchall():
#                 data.append((row.endpoint, row.owner, row.url))
#
#             return html(
#                 template_generators.all_links_page_generator(data),
#                 status=200
#             )
#
#     except Exception as error:
#         print(error)
#         return json({'message': 'getting links failed'}, status=500)
