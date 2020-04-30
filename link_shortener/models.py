'''
Copyright (C) 2020 Link Shortener Authors (see AUTHORS in Documentation).
Licensed under the MIT (Expat) License (see LICENSE in Documentation).
'''
from sqlalchemy import MetaData, Table, Column, String, Integer, BLOB, Text


metadata = MetaData()
actives = Table(
    'active_links',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('identifier', String(36)),
    Column('owner', String(50)),
    Column('owner_id', String(255)),
    Column('password', Text, default=None),
    Column('endpoint', String(20), unique=True),
    Column('url', String(300))
)

inactives = Table(
    'inactive_links',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('identifier', String(36)),
    Column('owner', String(50)),
    Column('owner_id', String(255)),
    Column('password', Text, default=None),
    Column('endpoint', String(20)),
    Column('url', String(300))
)

salts = Table(
    'hash_salts',
    metadata,
    Column('identifier', String(36), primary_key=True),
    Column('salt', BLOB)
)