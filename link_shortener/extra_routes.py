'''
Copyright (C) 2020 Link Shortener Authors (see AUTHORS in Documentation).
Licensed under the MIT (Expat) License (see LICENSE in Documentation).
'''
from sanic import Blueprint
from sanic.response import html, redirect

from link_shortener.templates import template_loader
from link_shortener.commands.redirect import redirect_link
from link_shortener.core.exceptions import NotFoundException


extra_blueprint = Blueprint('extra')


@extra_blueprint.route('/<category>/<link_endpoint>', methods=['GET'])
async def redirect_categorised_link_view(request, category, link_endpoint):
    try:
        endpoint = category + '/' + link_endpoint
        target = await redirect_link(request, endpoint)
        if (target[:10] == '/authorize/'):
            return redirect(target)

        return html(template_loader(
                        template_file='redirect.html',
                        link=target,
                    ), status=307)
    except NotFoundException:
        return html(template_loader('message.html'), status=404)
