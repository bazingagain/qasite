import logging

from django.test import TestCase
from gensim import models

from qasite.app.word2vec.bean.doc2vec import Doc2Vec


class Word2VecTest(TestCase):
    def test_laod_word2vec_model(self):
        wordmodel = models.Word2Vec.load('./model/med250.model.bin')
        docmodel = Doc2Vec(wordmodel)
        print(docmodel.query('我是中国人'))
        print(docmodel.similarity("山西副省长贪污腐败开庭", "陕西村干部受贿违纪"))
        print(docmodel.similarity("山西副省长贪污腐败开庭", "股票基金增长"))
        self.assertIsNotNone(docmodel)

    def test_use_word2vec_model(self):
        logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
        model = models.Word2Vec.load('../model/med250.model.bin')
        while True:
            try:
                query = input()
                q_list = query.split()
                if len(q_list) == 1:
                    print("相似词前 100 排序")
                    res = model.most_similar(q_list[0], topn=100)
                    for item in res:
                        print(item[0] + "," + str(item[1]))
                elif len(q_list) == 2:
                    print("计算 Cosine 相似度")
                    res = model.similarity(q_list[0], q_list[1])
                    print(res)
                else:
                    print("%s之于%s，如%s之于" % (q_list[0], q_list[2], q_list[1]))
                    res = model.most_similar([q_list[0], q_list[1]], [q_list[2]], topn=100)
                    for item in res:
                        print(item[0] + "," + str(item[1]))
                print("----------------------------")
            except Exception as e:
                print(repr(e))

