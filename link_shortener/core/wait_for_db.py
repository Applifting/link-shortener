'''
Copyright (C) 2020 Link Shortener Authors (see AUTHORS in Documentation).
Licensed under the MIT (Expat) License (see LICENSE in Documentation).
'''
import time

from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

from link_shortener.core.initialise_db import engine_data

engine = create_engine(engine_data)


def wait_for_db():
    db_is_online = False
    while not db_is_online:
        try:
            with engine.connect() as connection:
                connection.execute("select 1")
                print("DB loaded.")
                db_is_online = True

        except OperationalError:
            print("Waiting for DB to load.")
            time.sleep(1)

        except Exception as e:
            raise Exception(e)


if __name__ == '__main__':
    wait_for_db()
