# Created by leon at 09/12/2017

import jieba
from numpy import *
from sklearn import preprocessing

class Doc2Vec():
    def __init__(self, word2vecmodel):
        self.word2vecmodel = word2vecmodel
        self.dimension = word2vecmodel.vector_size

    def query(self, content):
        if content is None or len(content) == 0: return None
        jieba.suggest_freq(('聚类', '分析'), True)
        termList = jieba.cut(content ,cut_all=True) # 全模式
        n = 0
        result = zeros(self.dimension)
        for term in termList:
            try:
                termVec = self.word2vecmodel.wv[term]
            except KeyError:
                continue
            n+=1
            result = result + termVec
        if n == 0:
            return None
        return preprocessing.normalize(mat(result))[0] # 归一化

    def similarity(self, a, b):
        va = self.query(a)
        if va is None: return float(-1)
        vb = self.query(b)
        if vb is None: return float(-1)
        return dot(va, vb) # va,vb均为归一化后的矩阵

