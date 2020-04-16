'''
Copyright (C) 2020 Link Shortener Authors (see AUTHORS in Documentation).
Licensed under the MIT (Expat) License (see LICENSE in Documentation).
'''
from sanic import Blueprint
from sanic.response import html, json


template_blueprint = Blueprint('templates')


@template_blueprint.route('/about')
async def about_template(request):
    try:
        base = open('src/templates/base.html', 'r').read()
        about = open('src/templates/about/about.html', 'r').read()
        return html(base + about)

    except Exception as error:
        print(error)
        return json({'message': 'getting route failed'}, status=500)
