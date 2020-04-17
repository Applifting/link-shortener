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
    all_links = open('src/templates/all/all_links.html', 'r').read()
    appendix = open('src/templates/all/all_links_appendix.html', 'r').read()
    page += base + all_links
    for row in queryset:
        page += all_table_row_generator(row[0], row[1], row[2])

    page += appendix
    return page


def my_links_page_generator(active_queryset, inactive_queryset):
    '''
    Generates an HTML representation of a table of all links of a single user
    from a queryset provided by the owner_specific_links coroutine (server.py).
    '''
    page = ''
    base = open('src/templates/base.html', 'r').read()
    my_links = open('src/templates/my/my_links.html', 'r').read()
    appendix = open('src/templates/my/my_links_appendix.html', 'r').read()
    page += base + my_links
    for row in active_queryset:
        page += my_table_row_generator(row[0], row[1], True)

    for row in inactive_queryset:
        page += my_table_row_generator(row[0], row[1], False)

    page += appendix
    return page


def my_table_row_generator(endpoint, url, active):
    '''
    Generates an HTML representation of a table row populated with
    input attributes.
    '''
    switch = 'red'
    status = 'Inactive'
    if active:
        switch = 'green'
        status = 'Active'

    table_row = '<tr> \
                 <td>/{}</td> \
                 <td><a href="{}">{}</a></td> \
                 <td>fueled.by/{}</td> \
                 <td style="color: {};">{}</td> \
                 </tr>'.format(endpoint, url, url, endpoint, switch, status)

    return table_row


def all_table_row_generator(endpoint, owner, url):
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
