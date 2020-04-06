import mysql.connector

from json import dumps

from sanic import Sanic
from sanic.response import json


app = Sanic()

mydb = mysql.connector.connect(
    host='db',
    user='root',
    passwd='password',
    database='cat_db'
)
mycursor = mydb.cursor()


@app.route('/get_db', methods=['GET'])
async def get_db(request):
    try:
        mycursor.execute('SHOW DATABASES')
        for x in mycursor:
            print(x)
        return json({'message': 'getting db successful'}, status=200)
    except Exception as error:
        print(error)
        return json({'message': 'getting db failed'}, status=500)


@app.route('/get_tables', methods=['GET'])
async def get_tables(request):
    try:
        mycursor.execute('SHOW TABLES')
        for x in mycursor:
            print(x)
        return json({'message': 'showing tables successful'}, status=200)
    except Exception as error:
        print(error)
        return json({'message': 'showing tables failed'}, status=500)


@app.route('/create_db', methods=['GET'])
async def create_db(request):
    try:
        mycursor.execute('CREATE DATABASE cat_db')
        return json({'message': 'creating db successful'}, status=201)
    except Exception as error:
        print(error)
        return json({'message': 'creating db failed'}, status=500)


@app.route('/create_table', methods=['GET'])
async def create_table(request):
    try:
        mycursor.execute('CREATE TABLE IF NOT EXISTS cats (name TEXT, age INT)')
        return json({'message': 'creating table successful'}, status=201)
    except Exception as error:
        print(error)
        return json({'message': 'creating table failed'}, status=500)


@app.route('/create_cat', methods=['POST'])
async def create_cat(request):
    try:
        data = request.json

        query = 'INSERT INTO cats (name, age) VALUES (%s, %s)'
        values = (data['name'], data['age'])
        mycursor.execute(query, values)
        mydb.commit()
        return json({'message': 'cat creation successful'}, status=201)

    except Exception as error:
        print(error)
        return json({'message': 'cat creation failed'}, status=500)


@app.route('/get_cats', methods=['GET'])
async def get_cats(request):
    try:
        mycursor.execute('SELECT * FROM cats')
        qs = mycursor.fetchall()
        data = dumps(qs)
        return json(data, status=200)
    except Exception as error:
        print(error)
        return json({'message': 'getting cats failed'}, status=500)


if (__name__ == '__main__'):
    app.run(host='0.0.0.0', port=8000)
