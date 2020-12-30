'''
Copyright (C) 2020 Link Shortener Authors (see AUTHORS in Documentation).
Licensed under the MIT (Expat) License (see LICENSE in Documentation).
'''


def filter_links(data, filters):
    owners = set(row['owner'] for row in data)

    if filters['owner']:
        data = [row for row in data if row['owner'] == filters['owner']]

    if filters['search']:
        data = [row for row in data if filters['search'] in row['endpoint']]

    if filters['created']:
        obj = [row for row in data if row['endpoint'] == filters['created']][0]
        new_link = data.pop(data.index(obj))
        data.insert(0, new_link)

    return {'owners': owners, 'data': data}


def get_filter_dict(request):
    filter_set = {'is_active', 'owner', 'search'}
    data = request.args
    created_param = [t[1] for t in request.query_args if t[0] == 'created']

    filters = {element: data.get(element, None) for element in filter_set}
    if filters['is_active'] == 'false':
        filters['is_active'] = False
    else:
        filters['is_active'] = True

    filters['created'] = created_param[0] if len(created_param) == 1 else None

    return filters
