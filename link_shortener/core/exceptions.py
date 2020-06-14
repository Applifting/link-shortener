'''
Copyright (C) 2020 Link Shortener Authors (see AUTHORS in Documentation).
Licensed under the MIT (Expat) License (see LICENSE in Documentation).
'''
class AccessDeniedException(Exception):
    '''
    Used for API token checking. Raised when headers are missing a token
    or the token is incorrect.
    '''
    pass


class DuplicateActiveLinkForbidden(Exception):
    '''
    Used when link activation is attempted. Raised when an active link with
    the same endpoint already exists.
    '''
    pass
