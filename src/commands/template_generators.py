'''
Copyright (C) 2020 Link Shortener Authors (see AUTHORS in Documentation).
Licensed under the MIT (Expat) License (see LICENSE in Documentation).
'''
def all_links_page_generator(queryset):
    '''
    Generates an HTML representation of a table of all active links
    from a queryset provided by the get_active_links coroutine (server.py).
    '''
    page = ''
    base = open('src/templates/base.html', 'r').read()
    all_links = open('src/templates/all_links.html', 'r').read()
    appendix = open('src/templates/all_links_appendix.html', 'r').read()
    page += base + all_links
    for row in queryset:
        page += table_row_generator(row[0], row[1], row[2])

    page += appendix
    return page


def table_row_generator(endpoint, owner, url):
    '''
    Generates an HTML representation of a table row populated with
    input attributes.
    '''
    table_row = '<tr> \
                 <td>/{}</td> \
                 <td>{}</td> \
                 <td><a href="{}">{}</a></td> \
                 <td>fueled.by/{}</td> \
                 </tr>'.format(endpoint, owner, url, url, endpoint)

    return table_row
