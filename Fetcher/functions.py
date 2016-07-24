#!usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
import re
import logging
logger = logging.getLogger(__name__)
stream_handler = logging.StreamHandler()
logger.setLevel(logging.DEBUG)
stream_handler.setLevel(logging.INFO)
file_handler = logging.FileHandler(filename='log.txt')
file_handler.setLevel(logging.DEBUG)
logger.addHandler(file_handler)
logger.addHandler(stream_handler)

from collections import namedtuple

pageinfo = namedtuple("pageinfo", ["url", "degree", "body"])

INFOS = set()
WIKI_PATTERN = re.compile("^(/wiki/)((?!:).)*$")
URLS = set()


def _extractcontent(html):
    return html.get_text().replace(' ', '').replace("\n", '').replace("　", '')


def crowl(url, degree=2):
    """特定のhtmlから全てのリンクを取得する

    Args:
        url (str): 取得したいhtmlのurl
    Yields:
        set (str): リンク先のurl
    """
    global URLS
    global INFOS

    result = requests.get(url)
    html = result.text

    print("\t".join([url, str(degree), html]))
    bsObj = BeautifulSoup(html)
    body_content = bsObj.find("div", {"id": "bodyContent"})
    logger.debug("body content is {} and class it's class is {}".
                 format(body_content, body_content.__class__))

    content = _extractcontent(body_content)
    INFOS.add(pageinfo(url, degree, content))

    if degree == 0:
        return
    degree -= 1

    for link in body_content.findAll("a",  href=WIKI_PATTERN):
        if 'href' in link.attrs:
            if link.attrs['href'] not in URLS:
                new_url = link.attrs['href']
                logger.info("found new page {} !!".format(new_url))
                URLS.add(new_url)
                crowl("http://ja.wikipedia.org{}".format(new_url),
                             degree=degree)


if __name__ == '__main__':
    crowl("https://ja.wikipedia.org/wiki/Pok%C3%A9mon_GO", degree=1)
    with open("result.csv", "w") as fh:
        for info in INFOS:
            fh.write(",".join([info.url, str(info.degree), info.body, "\n"]))
