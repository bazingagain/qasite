# Created by leon at 09/12/2017

# -*- coding: utf-8 -*-

import jieba
import logging
from qasite import settings
from gensim.corpora import WikiCorpus

def segment():
    """
    对中文维基百科的内容进行分词处理
    :return:
    """
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    # 加载自定义的词典
    # jieba.set_dictionary(settings.BASE_DIR+'/data/dict/dict.txt.big')
    # 加载停用词
    stopwordset = set()
    with open(settings.BASE_DIR+'/data/dict/stopwords.txt','r',encoding='utf-8') as sw:
        for line in sw:
            stopwordset.add(line.strip('\n'))
    texts_num = 0
    output = open(settings.BASE_DIR+'/data/train/wiki_seg.txt','w')
    with open(settings.BASE_DIR+'/data/train/wiki_texts.txt','r') as content :
        for line in content:
            line = line.strip('\n')
            words = jieba.cut(line, cut_all=False)
            for word in words:
                if word not in stopwordset:
                    output.write(word +' ')
            texts_num += 1
            if texts_num % 10000 == 0:
                logging.info("已完成前 %d 行的断词" % texts_num)
    output.close()

def wiki_to_txt(wikiFileName):
    """
    将中文维基百科转换为txt文件
    https://dumps.wikimedia.org/zhwiki/20170920/
    :param wikiFileName: zhwiki-20160820-pages-articles.xml.bz2
    :return:
    """
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    wiki_corpus = WikiCorpus(wikiFileName, dictionary={})
    texts_num = 0

    with open(settings.BASE_DIR+'/data/train/wiki_texts.txt', 'w', encoding='utf-8') as output:
        for text in wiki_corpus.get_texts():
            output.write(' '.join(text) + '\n')
            texts_num += 1
            if texts_num % 10000 == 0:
                logging.info("处理 %d 篇文章" % texts_num)

if __name__ == '__main__':
    wiki_to_txt(settings.BASE_DIR+'/data/train/zhwiki-20170920-pages-articles.xml.bz2')
    segment()
