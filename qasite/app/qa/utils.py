# Created by leon at 24/12/2017
from numpy import *
from qasite import settings

import jieba.posseg as pseg

def senetnceVectorDistance(va, vb):
    if va is None or vb is None:
        return float(-1)
    else:
        return dot(va, vb)

def jiebaCutTest():
    words = pseg.cut("IMF国际组织简称是什么")
    for word, flag in words:
        print('%s %s' % (word, flag))


def getClusterQuestion():
    with open(settings.BASE_DIR + '/data/test/clusterquestion.txt', 'r') as fr,\
            open(settings.BASE_DIR + '/data/test/question.txt', 'w') as fw:
        for line in fr.readlines():
            print(line.split('--')[0])
            fw.writelines(line.split('--')[0])
            fw.writelines('\n')


if __name__=='__main__':
    jiebaCutTest()







