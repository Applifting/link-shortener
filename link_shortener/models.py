'''
Copyright (C) 2020 Link Shortener Authors (see AUTHORS in Documentation).
Licensed under the MIT (Expat) License (see LICENSE in Documentation).
'''
from sqlalchemy import (MetaData, Table, Column, ForeignKey, String, Integer,
                        BLOB, Date, Boolean)


metadata = MetaData()
links = Table(
    'links',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('owner', String(50)),
    Column('owner_id', String(255)),
    Column('password', BLOB, default=None),
    Column('endpoint', String(20)),
    Column('url', String(300)),
    Column('switch_date', Date, default=None),
    Column('is_active', Boolean, default=False)
)
salts = Table(
    'hash_salts',
    metadata,
    Column(
        'link_id',
        Integer,
        ForeignKey('links.id', onupdate='CASCADE', ondelete='CASCADE')
    ),
    Column('salt', BLOB)
)
