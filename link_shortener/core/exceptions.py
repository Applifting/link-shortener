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


class NotFoundException(Exception):
    '''
    Used when retrieving a specific link from the database via its ID.
    Raised when no link with the specified ID exists.
    '''
    pass


class FormInvalidException(Exception):
    '''
    Used on a POST request to a form. Raised when the form is not valid.
    '''
    pass


class MissingDataException(Exception):
    '''
    Used while checking request data from a POST request. Raised when one
    or more mandatory attributes do not have a value.
    '''
    pass


class IncorrectDataFormat(Exception):
    '''
    Used while processing request data from a POST request. Raised when
    an attribute has an incorrect format.
    '''
    pass
