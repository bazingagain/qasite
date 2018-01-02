# Created by leon at 09/12/2017

from gensim.models import word2vec
import logging
import jieba

def main():

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    sentences = word2vec.Text8Corpus("../data/wiki_seg.txt")
    model = word2vec.Word2Vec(sentences, size=250)

    #保存模型
    model.save("../model/med250.model.bin")

    #模型获取
    # model = word2vec.Word2Vec.load("../model/med250.model.bin")

def test():
    # model = word2vec.Word2Vec.load("../model/med250.model.bin")
    termList = jieba.cut('参数估计的点估计')  # 精确模式
    print(",".join(termList))
    termList = jieba.cut('参数估计的点估计', cut_all=True)  # 全模式
    print(",".join(termList))
    termList = jieba.cut('参数估计的点估', cut_all=True)  # 精确模式
    print(",".join(termList))
    # for term in termList:
    #     print(term)
    # print(model.wv['分析'])
if __name__ == "__main__":
    # main()
    test()
