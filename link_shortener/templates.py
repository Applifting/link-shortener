'''
Copyright (C) 2020 Link Shortener Authors (see AUTHORS in Documentation).
Licensed under the MIT (Expat) License (see LICENSE in Documentation).
'''
from decouple import config
from jinja2 import Environment, PackageLoader


def template_loader(template_file, *args, **kwargs):
    '''
    Loads and renders Django-style templates using Jinja.
    '''
    file_loader = PackageLoader(__name__, 'templates')
    env = Environment(loader=file_loader)
    template = env.get_template(template_file)
    analytics_id = config('ANALYTICS_ID')
    analytics_dsn = config('ANALYTICS_DSN')
    output = template.render(*args, **kwargs,
                             analytics_id=analytics_id,
                             analytics_dsn=analytics_dsn
                             )
    return output
