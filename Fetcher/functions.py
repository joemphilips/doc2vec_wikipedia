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
file_handler = logging.FileHandler(filename = 'log.txt')
file_handler.setLevel(logging.DEBUG)
logger.addHandler(file_handler)
logger.addHandler(stream_handler)


def extract_link(url):
    """特定のhtmlから全てのリンクを取得する

    Args:
        url (str): 取得したいhtmlのurl
    Yields:
        str: リンク先のurl
    """
    result = requests.get(url)
    html = result.text
    bsObj = BeautifulSoup(html)
    wiki_pattern = re.compile("^(/wiki/)((?!:).)*$")
    body_content = bsObj.find("div", {"id": "bodyContent"})
    logger.debug("body content is {} ".format(body_content))
    for link in body_content.findAll("a",  href=wiki_pattern):
        if 'href' in link.attrs:
            yield link.attrs['href']


def crowl(url, degree=2):
    """urlからdegree内のリンクを全てたどりそのhtmlをダウンロードする。"""
    for link in extract_link(url):
        degree -= 1




if __name__ == '__main__':
    extract_link("http://en.wikipedia.org/wiki/Pok%C3%A9mon_Go")

