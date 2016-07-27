#!usr/bin/env python
# -*- coding: utf-8 -*-

from gensim.corpora import WikiCorpus
from gensim.corpora import MmCorpus
from gensim.models.doc2vec import TaggedDocument
from gensim.models import Doc2Vec
import MeCab
mecab = MeCab.Tagger('mecabrc')
mecab.parse("") # to avoid UnicodeDecodeError, see http://taka-say.hateblo.jp/entry/2015/06/24/183748
from lxml import etree # since bs4 cannot parse by iterator
import logging
logger = logging.getLogger(__name__)
formatter = logging.Formatter("%(asctime)s --- %(filename)s --- %(levelname)s --- %(message)s")
logger.setLevel(logging.DEBUG)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.ERROR)
file_handler = logging.FileHandler(filename = 'log.txt')
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.DEBUG)
logger.addHandler(stream_handler)
logger.addHandler(file_handler)

def make_corpus(path):
    wiki = WikiCorpus(path)
    MmCorpus.serialize('/mnt/ebs/wikidata/wiki_jp_vocab.mm', wiki)


def tagged_document_generator(wiki_xml):
    elementtree = etree.iterparse(wiki_xml)
    for i, content in enumerate(elementtree):
        event, element = content
        if not element.tag.endswith("text"):
            continue
        word_list = list(tokenize(element.text))
        yield TaggedDocument(word_list, [i])


def apply_doc2vec(teacher_data):
    model = Doc2Vec((t for t in tagged_document_generator(teacher_data)))
    model.save("/mnt/ebs/tmp/test_model")
    model.save_word2vec_format("/mnt/ebs/tmp/test_model.word2vecformat")


def tokenize(text):
    node = mecab.parseToNode(text)
    while node:
        if node.feature.split(',')[0] == '名詞':
            try:
                yield node.surface.lower()
            except UnicodeDecodeError as e:
                logger.warn("there was UnicodeDecodeError when parsing".format(node.surface))
                raise
        node = node.next


if __name__ == '__main__':
    apply_doc2vec("/mnt/ebs/wikidata/jawiki-latest-pages-articles.xml")
