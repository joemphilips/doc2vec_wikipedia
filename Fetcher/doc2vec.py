#!usr/bin/env python
# -*- coding: utf-8 -*-
from Fetcher.graph_matrix import get_all_link_list
from gensim.corpora import WikiCorpus
from gensim.corpora import MmCorpus
from gensim.models.doc2vec import TaggedDocument
from gensim.models import Doc2Vec
from glob import glob
import multiprocessing as mp
import MeCab
import re
import csv
mecab = MeCab.Tagger('-Ochasen')
mecab.parse("") # to avoid UnicodeDecodeError, see http://taka-say.hateblo.jp/entry/2015/06/24/183748
from lxml import etree # since bs4 cannot parse by iterator
import logging
logger = logging.getLogger(__name__)
formatter = logging.Formatter("%(asctime)s --- %(filename)s --- %(levelname)s --- %(message)s")
logger.setLevel(logging.DEBUG)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
file_handler = logging.FileHandler(filename = '/mnt/ebs/tmp/{}_log.txt'.format(__name__))
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.DEBUG)
logger.addHandler(stream_handler)
logger.addHandler(file_handler)
from psutil import virtual_memory
import resource

TOTAL_MEMORY = virtual_memory().total
CORES = mp.cpu_count() - 1 if mp.cpu_count() > 1 else 1

NoGoodTextForLearning = object()


def make_corpus(path):
    wiki = WikiCorpus(path)
    MmCorpus.serialize('/mnt/ebs/wikidata/wiki_jp_vocab.mm', wiki)


def tagged_document_generator(wiki_xml):
    logger.info("start parsing {} ...".format(wiki_xml))
    elementtree = etree.iterparse(wiki_xml)
    for i, content in enumerate(elementtree):
        # return if it reaches too much memory usage
        if i == 1000: # and resource.getrusage(resource.RUSAGE_SELF).ru_maxrss > TOTAL_MEMORY - 500000:
            return

        if i % 10000 == 0:
            logger.info("parsed {} documents ...".format(i))
        event, element = content
        if not element.tag.endswith("text"):
            continue
        title, cleantext = cleanup_text(element.text)
        if title == NoGoodTextForLearning:
            continue
        word_list = list(tokenize(cleantext))
        logger.debug("going to make TaggedDocument from {} ... and {} ".format(word_list[0:10], title))
        yield TaggedDocument(word_list, [title])


def cleanup_text(rawtext):
    """
    Examples::

        >>> cleanup_text(r" '''バスク語'''\n* [[バスク語]] ({{lang|eu|Euskara}}) の[[ISO 639|ISO 639-1言語コード]]")
		... ('バスク語', " バスク語 langeuEuskara のISO 639ISO-1言語コード")
    """
    try:
        title = re.search("\'\'\'.*?\'\'\'", rawtext).group().replace("\'", "")
    except AttributeError as e:
        logger.debug("cound not find title for {} ".format(rawtext))
        return (NoGoodTextForLearning, None)
    except TypeError as e:
        logger.error("raw text was not byte or text-like object, it was {} ".format(rawtext))
        return (NoGoodTextForLearning, None)
    cleantext =  re.sub(r"[\*|\[|\]|\{|\}\(|\)|\||\"|\']", "", rawtext) # TODO: there should be better way than this
    return (title, cleantext)


def train(teacher_data, save_file=True):
    if TOTAL_MEMORY < 2000000000:
        logger.warn("you would better have more than 2GB memory to train doc2ved !!")
    model = Doc2Vec(workers=CORES,
                    max_vocab_size=TOTAL_MEMORY / 12000,
                    size=50,
                    min_count=5,
                    iter=5)
    logger.info("starting to build vocablarries")
    model.build_vocab((t for t in tagged_document_generator(teacher_data)))
    logger.info("finished building vocablarries so goint go train model")
    model.train((t for t in tagged_document_generator(teacher_data)))
    if save_file == True:
        logger.info("finished training models so goint save in file")
        model.save("/mnt/ebs/tmp/test_model")
        model.save_word2vec_format("/mnt/ebs/tmp/test_model.word2vecformat")
    return model


def tokenize(text):
    textobj = text # to prevent segfault, see https://shogo82148.github.io/blog/2012/12/15/mecab-python/
    node = mecab.parseToNode(textobj)
    while node:
        if node.feature.split(',')[0] == '名詞':
            try:
                yield node.surface.lower()
            except UnicodeDecodeError as e:
                logger.exception("there was UnicodeDecodeError when parsing {} ".format(node.surface))
                raise
        node = node.next


def write_result_vector(model, htmldir, output_csv):
    logging.info("going to write result to {} ".format(output_csv))
    link_list = get_all_link_list(htmldir)
    htmlpaths = glob(htmldir + "/*html")
    with open(output_csv, "w") as csvfh:
        vec_writer = csv.writer(csvfh, delimiter=",")
        for h in htmlpaths:
            with open(h) as fh:
                html = fh.read()
            vector = model.infer_vector(html)
            vec_writer.writerow( [h.split("/")[-1].split(".")[0]] + [ str(f) for f in vector ])



if __name__ == "__main__":
    # import doctest
    # doctest.testmod()
    trained_model = train("/mnt/ebs/wikidata/jawiki-latest-pages-articles.xml", save_file=False)
    write_result_vector(trained_model, "/mnt/ebs/tmp", "result_vector.csv")

