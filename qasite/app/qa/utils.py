# Created by leon at 24/12/2017
from numpy import *

import jieba.posseg as pseg

def senetnceVectorDistance(va, vb):
    if va is None or vb is None:
        return float(-1)
    else:
        return dot(va, vb)


def jiebaCutTest():
    words = pseg.cut("我爱北京天安门")
    for word, flag in words:
        print('%s %s' % (word, flag))

if __name__=='__main__':
    jiebaCutTest()






