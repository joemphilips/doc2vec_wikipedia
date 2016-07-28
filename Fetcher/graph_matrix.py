#!usr/bin/env python
# -*- coding: utf-8 -*-
from glob import glob
from Fetcher.functions import extract_body, WIKI_PATTERN
from collections import OrderedDict
import csv
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


def examine_haslink(html, all_link):
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
        has_link_dict[l] = 1 if l in links else 0
    return has_link_dict


def graph_matrix(html_file_dir="/mnt/ebs/tmp", outputfile="graph.csv"):
    all_link = get_all_link_list(html_file_dir)
    html_file_paths = glob("/mnt/ebs/tmp" + '/*html')
    with open(outputfile, "w") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = all_link)
        writer.writeheader()
        for i, html_path in enumerate(html_file_paths):
            with open(html_path) as fh:
                html = fh.read()
            has_link_or_not = examine_haslink(html, all_link)
            writer.writerow(has_link_or_not)


if __name__ == '__main__':
    graph_matrix()
