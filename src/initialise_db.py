'''
Copyright (C) 2020 Link Shortener Authors
Licensed under the MIT (Expat) License. See the LICENSE file found in the
top-level directory of this distribution.


Creates and populates a new table with links and their endpoints.
'''
import asyncio
import aiomysql


async def initialise_database():
    conn = await aiomysql.connect(
        host='db',
        port=3306,
        user='user',
        password='password',
        db='db',
        loop=loop
    )
    db_cursor = await conn.cursor()
    await db_cursor.execute(
        'CREATE TABLE IF NOT EXISTS links (endpoint TEXT, url TEXT)'
    )
    query = 'INSERT INTO links (endpoint, url) VALUES (%s, %s)'
    data = [
        ('google', 'https://www.google.com/'),
        ('pomuzemesi', 'https://staging.pomuzeme.si'),
        ('epark', 'https://www.eparkomat.com/app/'),
        ('vlk', 'http://www.vlk.cz'),
        ('kodex', 'https://github.com/Applifting/culture'),
        ('meta', 'https://github.com/Applifting/link-shortener')
    ]
    await db_cursor.executemany(query, data)
    await conn.commit()

    await db_cursor.close()
    conn.close()


loop = asyncio.get_event_loop()
loop.run_until_complete(initialise_database())
