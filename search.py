#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from workflow import Workflow3, web

API_URL = 'https://crates.io/api/v1'

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)'
}


def search(wf, limit=10):
    if len(wf.args) >= 1:
        query = wf.args[0]
        resp = web.get('%s/crates?q=%s&page=%d' % (API_URL, query, 1), headers=HEADERS).json()
        total = resp['meta']['total']
        count = 0
        pages = (total - 1) / 10 + 1
        for page in range(1, pages):
            for c in resp['crates']:
                count = count + 1
                item = wf.add_item(title='%s[v%s]' % (c['id'], c['max_version']),
                                   subtitle=c['description'],
                                   valid=True,
                                   arg=c['id'])
                item.add_modifier(key='cmd',
                                  subtitle='Copy the config to clipboard',
                                  arg='%s = \"%s\"' % (c['name'], c['max_version']))
                item.add_modifier(key='alt',
                                  subtitle='Open the repository of [%s]' % c['name'],
                                  arg=c['repository'])
                item.add_modifier(key='fn',
                                  subtitle='Open the documentation of [%s]' % c['name'],
                                  arg=c['documentation'])
            if count >= limit:
                break
            else:
                resp = web.get('%s/crates?q=%s&page=%d' % (API_URL, query, page + 1), headers=HEADERS).json()

    wf.send_feedback()


if __name__ == '__main__':
    wf = Workflow3()
    sys.exit(wf.run(search))
