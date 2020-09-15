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

    return {"owners": owners, "data": data}