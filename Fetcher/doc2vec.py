#!usr/bin/env python
# -*- coding: utf-8 -*-

from gensim.corpora import WikiCorpus
from gensim.corpora import MmCorpus
from gensim.models.doc2vec import TaggedDocument
from gensim.models import Doc2Vec
import MeCab
import re
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


class NoGoodTextForLearning:
    pass


def make_corpus(path):
    wiki = WikiCorpus(path)
    MmCorpus.serialize('/mnt/ebs/wikidata/wiki_jp_vocab.mm', wiki)


def tagged_document_generator(wiki_xml):
    logger.info("start parsing {} ...".format(wiki_xml))
    elementtree = etree.iterparse(wiki_xml)
    for i, content in enumerate(elementtree):
        if i % 1000 == 0:
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

        >>> cleanup_text(" '''バスク語'''\n* [[バスク語]] ({{lang|eu|Euskara}}) の[[ISO 639|ISO 639-1言語コード]]")
		... ('バスク語', " バスク語 langeuEuskara のISO 639ISO-1言語コード")
    """
    try:
        title = re.search("\'\'\'.*\'\'\'", rawtext).group().replace("\'", "")
    except AttributeError as e:
        logger.debug("cound not find title for {} ".format(rawtext))
        return (NoGoodTextForLearning, None)
    except TypeError as e:
        logger.error("raw text was not byte or text-like object, it was {} ".format(rawtext))
        return (NoGoodTextForLearning, None)
    cleantext =  re.sub(r"[\*|\[|\]|\{|\}\(|\)|\||\"|\']", "", rawtext) # TODO: there should be better way than this
    return (title, cleantext)


def apply_doc2vec(teacher_data):
    model = Doc2Vec((t for t in tagged_document_generator(teacher_data)))
    model.save("/mnt/ebs/tmp/test_model")
    model.save_word2vec_format("/mnt/ebs/tmp/test_model.word2vecformat")


def tokenize(text):
    textobj = text # to prevent segfault, see https://shogo82148.github.io/blog/2012/12/15/mecab-python/
    node = mecab.parseToNode(textobj)
    while node:
        if node.feature.split(',')[0] == '名詞':
            try:
                yield node.surface.lower()
            except UnicodeDecodeError as e:
                logger.warn("there was UnicodeDecodeError when parsing {} ".format(node.surface))
                raise
        node = node.next


if __name__ == '__main__':
    apply_doc2vec("/mnt/ebs/wikidata/jawiki-latest-pages-articles.xml")
