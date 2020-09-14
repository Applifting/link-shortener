'''
Copyright (C) 2020 Link Shortener Authors (see AUTHORS in Documentation).
Licensed under the MIT (Expat) License (see LICENSE in Documentation).
'''
import time

from decouple import config
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError


def test_db():
    try:
        if config('PRODUCTION', default=False, cast=bool):
            engine = create_engine(
                f"mysql+pymysql://"
                f"{config('MYSQL_USER')}:"
                f"{config('MYSQL_PASSWORD')}@"
                f"{config('MYSQL_HOST')}:"
                f"{config('MYSQL_PORT', cast=int)}/"
                f"{config('MYSQL_DB')}"
            )

        else:
            engine = create_engine(
                "mysql+pymysql://user:password@db:3306/db"
            )

        engine.begin()

    except OperationalError:
        print("Waiting for DB to load.")
        time.sleep(2)
        test_db()

    except Exception as e:
        raise Exception(e)

    print("DB loaded. Starting up the server")

    
if __name__ == '__main__'
    test_db()
