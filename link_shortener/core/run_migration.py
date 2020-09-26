'''
Copyright (C) 2020 Link Shortener Authors (see AUTHORS in Documentation).
Licensed under the MIT (Expat) License (see LICENSE in Documentation).
'''

from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine

from link_shortener.core.initialise_db import engine_data

alembic_cfg = Config("./alembic.ini")

engine = create_engine(engine_data)


def run_migration():
    with engine.begin() as connection:
        print("Running migration")
        alembic_cfg.attributes['connection'] = connection
        command.upgrade(alembic_cfg, "head")
        print("Migration completed")


if __name__ == '__main__':
    run_migration()
