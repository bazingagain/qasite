# Created by leon at 09/12/2017

import logging

import jieba
import mysql.connector
from gensim.models import word2vec

from qasite import settings
from qasite.app.word2vec.bean import doc2vec


def trainWord2vecFromWiki():
    """
    使用中文wiki的分词后的语料,训练出word2vec的模型
    :return:
    """
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    sentences = word2vec.Text8Corpus(settings.BASE_DIR+"/data/train/wiki_seg.txt")
    model = word2vec.Word2Vec(sentences, size=250)
    model.save(settings.WORD2VEC_MODEL_FILE)

def trainDoc2vecFromFAQ():
    """
    使用数据库中的FAQ,训练处每个问题的句子向量
    :return:
    """
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    wordmodel = word2vec.Word2Vec.load(settings.WORD2VEC_MODEL_FILE)
    docmodel = doc2vec.Doc2Vec(wordmodel)
    output = open(settings.QAPAIR_VEC_FILE, 'w')
    con = mysql.connector.connect(user=settings.DATABASES['default']['USER'],
                                  password=settings.DATABASES['default']['PASSWORD'],
                                  database=settings.DATABASES['default']['NAME'])
    cursor = con.cursor()
    cursor.execute('select * from qa_qapair')
    values = cursor.fetchall()
    for v in values:
        index = str(v[0])
        question = v[1]
        classLabel = v[8]
        vec = docmodel.query(question)
        if vec is None:
            logging.error(index + ' ' + question)
        else:
            output.write(index)
            for v in vec:
                output.write(' ' + str(v))
            output.write(' ' + classLabel)
            output.write('\n')
    output.close()

def test():
    model = word2vec.Word2Vec.load(settings.WORD2VEC_MODEL_FILE)
    termList = jieba.cut('参数估计的点估计')  # 精确模式
    print(",".join(termList))
    termList = jieba.cut('参数估计的点估计', cut_all=True)  # 全模式
    print(",".join(termList))
    termList = jieba.cut('参数估计的点估', cut_all=True)  # 精确模式
    print(",".join(termList))
    print(model.wv['分析'])


if __name__ == "__main__":
    # trainWord2vecFromWiki()
    trainDoc2vecFromFAQ()
