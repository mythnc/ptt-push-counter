#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import sys
from collections import Counter
import requests
from pyquery import PyQuery as pq


def get_requests_data(url):
    error_503 = '503 Service Temporarily Unavailable'
    while True:
        try:
            r = requests.get(url)
            s = pq(r.text)
            #time.sleep(0.2)
            if error_503 in s('title').text():
                print('503 error right now')
                sys.exit(1)
            return s
        except lxml.etree.XMLSyntaxError:
            print('XMLSyntaxError')
        except requests.exceptions.ConnectionError:
            print('ConnectionError')
            continue


def get_push_ids(url):
    s = get_requests_data(url)

    return s('#main-content > .push > .push-userid')\
            .map(lambda i, e: pq(this).text())


def count(users):
    cnt = Counter()
    for user in users:
        cnt[user] += 1

    for data in cnt.most_common():
        print('{} {}'.format(data[0], data[1]))


if __name__ == '__main__':
    url = sys.argv[1]
    users = get_push_ids(url)
    cnt = count(users)
