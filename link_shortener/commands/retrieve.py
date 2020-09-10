'''
Copyright (C) 2020 Link Shortener Authors (see AUTHORS in Documentation).
Licensed under the MIT (Expat) License (see LICENSE in Documentation).
'''
from link_shortener.models import links

from link_shortener.core.exceptions import NotFoundException


async def retrieve_links(request, filters):
    async with request.app.engine.acquire() as conn:
        link_select = links.select()
        for filter in filters.items():
            if filter[1] is not None:
                link_select = link_select.where(
                    links.columns[filter[0]] == filter[1]
                )
        queryset = await conn.execute(link_select)
        data = []
        for link in await queryset.fetchall():
            link_data = {
                'id': link.id,
                'owner': link.owner,
                'owner_id': link.owner_id,
                'endpoint': link.endpoint,
                'url': link.url,
                'is_active': link.is_active
            }
            if link.switch_date:
                link_data['switch_date'] = {
                    'Year': link.switch_date.year,
                    'Month': link.switch_date.month,
                    'Day': link.switch_date.day
                }
            data.append(link_data)

        return data


async def retrieve_link(request, link_id):
    async with request.app.engine.acquire() as conn:
        try:
            query = await conn.execute(links.select().where(
                links.columns['id'] == link_id
            ))
            link_data = await query.fetchone()
            data = {
                'id': link_data.id,
                'owner': link_data.owner,
                'owner_id': link_data.owner_id,
                'endpoint': link_data.endpoint,
                'url': link_data.url,
                'is_active': link_data.is_active
            }
            if link_data.switch_date:
                data['switch_date'] = {
                    'Year': link_data.switch_date.year,
                    'Month': link_data.switch_date.month,
                    'Day': link_data.switch_date.day
                }

            return data

        except AttributeError:
            raise NotFoundException
