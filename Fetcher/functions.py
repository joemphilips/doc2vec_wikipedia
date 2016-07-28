#!usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
import re
from collections import namedtuple
import logging
logger = logging.getLogger(__name__)

import multiprocessing as mp

pageinfo = namedtuple("pageinfo", ["url", "degree", "html"])

WIKI_PATTERN = re.compile("^(/wiki/)((?!:).)*$")
URLS = set()


def extract_body(html):
    bsObj = BeautifulSoup(html)
    return bsObj.find('div', {"id": "bodyContent"})

def extract_text(html):
    body_content = extract_body(html)
    return body_content.get_text().replace(' ', '').replace("\n", '').replace("　", '')

def crowl(url, q, degree=2, lang="ja"):
    """特定のhtmlから全てのリンクを取得する

    Args:
        url (str): 取得したいhtmlのurl
    Sets:
        set (str): リンク先のurl
    """
    global URLS

    result = requests.get(url)
    html = result.text
    q.put(pageinfo(url, degree, html))


    if degree == 0:
        return
    degree -= 1

    body_content = extract_body(html)

    for link in body_content.findAll("a",  href=WIKI_PATTERN):
        if 'href' in link.attrs:
            if link.attrs['href'] not in URLS:
                new_url = link.attrs['href']
                logger.info("found new page {} !!".format(new_url))
                URLS.add(new_url)
                crowl("http://{}.wikipedia.org{}".format(lang, new_url),
                      q=q,
                      degree=degree)


