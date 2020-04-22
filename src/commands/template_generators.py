'''
Copyright (C) 2020 Link Shortener Authors (see AUTHORS in Documentation).
Licensed under the MIT (Expat) License (see LICENSE in Documentation).
'''
from decouple import config


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
        page += all_table_row_generator(row[0], row[1], row[2], row[3])

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
        page += my_table_row_generator(row[0], row[1], row[2], True)

    for row in inactive_queryset:
        page += my_table_row_generator(row[0], row[1], row[2], False)

    page += appendix
    return page


def my_table_row_generator(id, endpoint, url, active):
    '''
    Generates an HTML representation of a table row populated with
    input attributes.
    '''
    if active:
        table_row = '<tr> \
                     <td>/{endpoint}</td> \
                     <td><a href="{url}">{url}</a></td> \
                     <td>{domain_name}/{endpoint}</td> \
                     <td><a href="/deactivate/{id}"> \
                     <img src="on.png" heigh="20" width="20"></a></td> \
                     <td><a href="/edit/active/{id}"> \
                     <img src="edit.png" heigh="20" width="20"></a></td> \
                     <td><a href="/delete/active/{id}"> \
                     <img src="delete.png" heigh="20" width="20"></a></td> \
                     </tr>'.format(
                        endpoint=endpoint,
                        url=url,
                        domain_name=config('DOMAIN_NAME'),
                        id=id
                    )

    else:
        table_row = '<tr> \
                     <td>/{endpoint}</td> \
                     <td><a href="{url}">{url}</a></td> \
                     <td>{domain_name}/{endpoint}</td> \
                     <td><a href="/activate/{id}"> \
                     <img src="off.png" heigh="20" width="20"></a></td> \
                     <td><a href="/edit/inactive/{id}"> \
                     <img src="edit.png" heigh="20" width="20"></a></td> \
                     <td><a href="/delete/inactive/{id}"> \
                     <img src="delete.png" heigh="20" width="20"></a></td> \
                     </tr>'.format(
                        endpoint=endpoint,
                        url=url,
                        domain_name=config('DOMAIN_NAME'),
                        id=id
                    )

    return table_row


def all_table_row_generator(id, endpoint, owner, url):
    '''
    Generates an HTML representation of a table row populated with
    input attributes.
    '''
    table_row = '<tr> \
                 <td>/{endpoint}</td> \
                 <td>{owner}</td> \
                 <td><a href="{url}">{url}</a></td> \
                 <td>{domain_name}/{endpoint}</td> \
                 <td><a href="/edit/active/{id}"> \
                 <img src="edit.png" heigh="20" width="20"></a></td> \
                 <td><a href="/delete/active/{id}"> \
                 <img src="delete.png" heigh="20" width="20"></a></td> \
                 </tr>'.format(
                    endpoint=endpoint,
                    owner=owner,
                    url=url,
                    domain_name=config('DOMAIN_NAME'),
                    id=id
                )

    return table_row
