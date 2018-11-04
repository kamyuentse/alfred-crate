#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from workflow import Workflow3, web

API_URL = 'https://crates.io/api/v1'

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
    'Accept': 'application/json'
}


def get_page(query, page=1):
    return web.get('%s/crates?q=%s&page=%d' % (API_URL, query, page), headers=HEADERS).json()


def search(wf, limit=10):
    if len(wf.args) >= 1:
        count = 0
        index = 1
        query = wf.args[0]
        items = get_page(query, index)
        total = min(items['meta']['total'], limit)
        while count < total:
            for crate in items['crates']:
                count = count + 1
                item = wf.add_item(title='%s[v%s]' % (crate['id'], crate['max_version']),
                                   subtitle=crate['description'],
                                   valid=True,
                                   arg=crate['id'])
                item.add_modifier(key='cmd',
                                  subtitle='Send config entry to clipboard',
                                  arg='%s = \"%s\"' % (crate['name'], crate['max_version']))
                item.add_modifier(key='alt',
                                  subtitle='Open documentation of [%s]' % crate['name'],
                                  arg=crate['documentation'])
                if count >= limit:
                    break
            index = index + 1
            items = get_page(query, index)

    wf.send_feedback()


if __name__ == '__main__':
    wf = Workflow3()
    sys.exit(wf.run(search))

