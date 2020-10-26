'''
Copyright (C) 2020 Link Shortener Authors (see AUTHORS in Documentation).
Licensed under the MIT (Expat) License (see LICENSE in Documentation).
'''
import re

from sqlalchemy import and_

from link_shortener.core.exceptions import (DuplicateActiveLinkForbidden,
                                            LinkNotAllowed)
from link_shortener.models import links


blacklisted_words = []


async def endpoint_duplicity_check(conn, data):
    query = await conn.execute(links.select().where(and_(
        links.columns['endpoint'] == data['endpoint'],
        links.columns['is_active'].is_(True)
    )))
    link_data = await query.fetchone()

    if link_data:
        raise DuplicateActiveLinkForbidden


def url_validation(url):
    '''
    Checks the URL for blacklisted patterns, then adds a subdomain unless
    it already has one.
    '''
    for word in blacklisted_words:
        pattern = re.compile(word, re.I)
        if pattern.search(url):
            raise LinkNotAllowed

    if url[:4] != 'http':
        url = 'http://' + url

    return url
