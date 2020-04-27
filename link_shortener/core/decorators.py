'''
Copyright (C) 2020 Link Shortener Authors (see AUTHORS in Documentation).
Licensed under the MIT (Expat) License (see LICENSE in Documentation).
'''
from functools import wraps
from decouple import config

from sanic.response import json


whitelist = [
    config('WHITELISTED_EMAIL_1'),
    config('WHITELISTED_EMAIL_2')
]


def credential_whitelist_check(original_func):

    @wraps(original_func)
    async def wrapper(request, user, *args, **kwargs):
        if (user.email.split('@')[1] in whitelist):
            response = await original_func(request, user, *args, **kwargs)
            return response
        else:
            return json({'message': 'unauthorized'}, status=401)

    return wrapper
