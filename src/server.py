'''
Copyright (C) 2020 Link Shortener Authors
Licensed under the MIT (Expat) License. See the LICENSE file found in the
top-level directory of this distribution.
'''
import mysql.connector

from json import dumps

from sanic import Sanic, response
from sanic.response import json


app = Sanic()

mydb = mysql.connector.connect(
    host='db',
    user='user',
    passwd='password',
    database='db'
)
mycursor = mydb.cursor()


@app.route('/api/links', methods=['GET'])
async def get_links(request):
    try:
        mycursor.execute('SELECT * FROM links')
        qs = mycursor.fetchall()
        data = dumps(qs)
        return json(data, status=200)
    except Exception as error:
        print(error)
        return json({'message': 'getting links failed'}, status=500)


@app.route('/<link_endpoint>')
async def redirect_link(request, link_endpoint):
    try:
        query = 'SELECT * FROM links WHERE endpoint = %s'
        value = (link_endpoint,)
        mycursor.execute(query, value)
        result = mycursor.fetchall()
        url = result[0][1]
        return response.redirect(url)
    except Exception as error:
        print(error)
        return json({'message': 'link does not exist'}, status=400)


if (__name__ == '__main__'):
    app.run(host='0.0.0.0', port=8000)
