'''
Copyright (C) 2020 Link Shortener Authors (see AUTHORS in Documentation).
Licensed under the MIT (Expat) License (see LICENSE in Documentation).
'''
import subprocess
import time

from decouple import config
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError


# Wait for connection with DB and if DB not empty run migration
def wait_for_db_and_check_migration():
    try:
        if config('PRODUCTION', default=False, cast=bool):
            engine = create_engine(f"postgresql://"
                                   f"{config('POSTGRES_USER')}:"
                                   f"{config('POSTGRES_PASSWORD')}@"
                                   f"{config('POSTGRES_HOST')}:"
                                   f"{config('POSTGRES_PORT')}/"
                                   f"{config('POSTGRES_DB')}"
                                   )

        else:
            engine = create_engine(
                'postgresql://postgres:postgres@db:5432/db'
            )

        # Retrieve DB status
        with engine.connect() as connection:
            count = connection.execute("select count(*) as tables from information_schema.tables "
                                              "where table_type = 'BASE TABLE' and table_schema = 'public'")
            count = count.fetchone()
            print("DB is online.")
            if count.tables:
                print("Running migration")
                subprocess.run(["alembic", "upgrade", "head"])
            else:
                print("DB is empty. Skipping migration.")

    except OperationalError:
        print("Waiting for DB to load.")
        time.sleep(1)
        wait_for_db_and_check_migration()

    except Exception as e:
        raise Exception(e)


if __name__ == '__main__':
    wait_for_db_and_check_migration()
