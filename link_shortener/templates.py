'''
Copyright (C) 2020 Link Shortener Authors (see AUTHORS in Documentation).
Licensed under the MIT (Expat) License (see LICENSE in Documentation).
'''
from jinja2 import Environment, PackageLoader


def template_loader(template_file, *args, **kwargs):
    '''
    Loads and renders Django-style templates using Jinja.
    '''
    file_loader = PackageLoader(__name__, 'jinja_templates')
    env = Environment(loader=file_loader)
    template = env.get_template(template_file)
    output = template.render(*args, **kwargs)
    return output
