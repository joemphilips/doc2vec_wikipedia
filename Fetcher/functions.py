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

url_with_degree = namedtuple("url_with_degree", ["url", "degree"])


class LinkExtracter:

    def __init__(self, url, degree=2):
        self.first_url = pages_with_degree(url, degree)
        self.all_urls = set()

    def __call__(self):
        self.extract_link(self.first_url)

    def extract_link(self, url):
        """特定のhtmlから全てのリンクを取得する

        Args:
            url (str): 取得したいhtmlのurl
        Yields:
            set (str): リンク先のurl
        """
        result = requests.get(url)
        html = result.text
        bsObj = BeautifulSoup(html)
        wiki_pattern = re.compile("^(/wiki/)((?!:).)*$")
        body_content = bsObj.find("div", {"id": "bodyContent"})
        logger.debug("body content is {} ".format(body_content))

        for link in body_content.findAll("a",  href=wiki_pattern):
            if 'href' in link.attrs:
                if link.attrs['href'] not in self.all_urls:
                    newPage = link.attrs['href']
                    logger.info("found new page {} !!".format(newPage))
                    PAGES.add(newPage)
                    extract_link(newPage)

URLS = set()
WIKI_PATTERN = re.compile("^(/wiki/)((?!:).)*$")


def extract_link(url, degree=2):
    """特定のhtmlから全てのリンクを取得する

    Args:
        url (str): 取得したいhtmlのurl
    Yields:
        set (str): リンク先のurl
    """
    global URLS

    result = requests.get(url)
    html = result.text

    print("\t".join(url, degree, html))
    URLS.add(url_with_degree(url, degree))
    degree -= 1

    bsObj = BeautifulSoup(html)
    body_content = bsObj.find("div", {"id": "bodyContent"})
    logger.debug("body content is {} ".format(body_content))

    for link in body_content.findAll("a",  href=WIKI_PATTERN):
        if 'href' in link.attrs:
            if link.attrs['href'] not in [u for u, _ in URLS]:
                newPage = link.attrs['href']
                logger.info("found new page {} !!".format(newPage))
                URLS.add(url_with_degree(newPage, degree - 1)
                extract_link(newPage, degree=degree)


# def crowl(url, degree=2):
#    """urlからdegree内のリンクを全てたどりそのhtmlをダウンロードする。"""
#    urls = []
#    for link in extract_link(url):
#        degree -= 1
#        urls.append(link)
#        extrac_link(link)




if __name__ == '__main__':
    extract_link("http://en.wikipedia.org/wiki/Pok%C3%A9mon_Go")

