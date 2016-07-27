#!usr/bin/env python
# -*- coding: utf-8 -*-
from glob import glob
from Fetcher.functions import extract_body, WIKI_PATTERN
from collections import OrderedDict
import logging
logger = logging.getLogger(__name__)
formatter = logging.Formatter("%(asctime)s --- %(filename)s --- %(levelname)s --- %(message)s")
logger.setLevel(logging.ERROR)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(filename = 'log.txt')
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.DEBUG)
logger.addHandler(stream_handler)
logger.addHandler(file_handler)

def get_all_link_list(path):
    return [ "/wiki/" + l.split("/")[-1].split('.')[0] for l in  glob(path + '/*.html')]


def graph_matrix(html, all_link):
    """
    Args:
        html (str): full html text
        all_link (list): all_link which could possibly be found in dataset
    Returns:
        OrderedDict:
            key (str): each of all_links
            value (bool): could be found in html or not
    """
    body_content = extract_body(html)
    logger.debug("\n\n\nbody_content is {} \n\n\n".format(body_content))
    has_link_dict = OrderedDict()
    links =  [l.attrs['href'] for l in body_content.findAll("a", href=WIKI_PATTERN) if 'href' in l.attrs]
    logger.debug("all_link are {} and links in documents are {}".format(all_link, links))
    for l in all_link:
        has_link_dict[l] = True if l in links else False
    return has_link_dict



if __name__ == '__main__':
    all_link = get_all_link_list("/mnt/ebs/tmp")
    for i, html_file_path in enumerate(glob("/mnt/ebs/tmp" + '/*html')):
        html_id = html_file_path.split("/")[-1].split('.')[0]
        with open(html_file_path) as fh:
            html = fh.read()
        has_link_or_not = graph_matrix(html, all_link)
        if i == 0:
            print("#id", ",", ",".join(['#' + str(k) for k in has_link_or_not.keys()])) # header
        print(html_id, ",", ",".join([ str(int(b)) for b in has_link_or_not.values()]))
