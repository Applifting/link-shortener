'''
Copyright (C) 2020 Link Shortener Authors
Licensed under the MIT (Expat) License. See the LICENSE file found in the
top-level directory of this distribution.


Creates and populates a new table with links and their endpoints.
'''
import mysql.connector


mydb = mysql.connector.connect(
    host='db',
    user='user',
    passwd='password',
    database='db'
)
mycursor = mydb.cursor()

mycursor.execute('CREATE TABLE IF NOT EXISTS links (endpoint TEXT, url TEXT)')

query = 'INSERT INTO links (endpoint, url) VALUES (%s, %s)'
values = [
    ('google', 'https://www.google.com/'),
    ('pomuzemesi', 'https://staging.pomuzeme.si'),
    ('epark', 'https://www.eparkomat.com/app/'),
    ('vlk', 'http://www.vlk.cz'),
    ('kodex', 'https://github.com/Applifting/culture'),
    ('meta', 'https://github.com/Applifting/link-shortener'),
]
mycursor.executemany(query, values)
mydb.commit()
