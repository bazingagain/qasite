# Created by leon at 12/12/2017

from sklearn import metrics
from sklearn.naive_bayes import GaussianNB
import joblib
import os
import logging
from numpy import *
from gensim import models
from qasite.app.word2vec.docvecmodel import Doc2Vec

class BayesClassifier:

    def __init__(self):
        self.classifier = GaussianNB()
        self.dataMat = None
        self.labelList = None

    def loadDataFromVecFile(self):
        logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
        pwd = __file__
        qapair_vecfile = os.path.join(os.path.abspath(os.path.dirname(pwd) + os.path.sep + "../../"), "cluster/data/qapair_vec.txt")
        clusterfile = os.path.join(os.path.abspath(os.path.dirname(pwd) + os.path.sep + "../../"), "cluster/data/clusterindex_8.txt")
        dataMat = []
        indexList = []
        qafr = open(qapair_vecfile)
        for line in qafr.readlines():
            curLine = line.strip().split(' ')
            indexList.append(curLine[0])
            curLine = curLine[1:]
            i = 0
            for s in curLine:
                curLine[i] = float(s)
                i += 1
            dataMat.append(curLine)
        clufr = open(clusterfile)
        labelList = []
        j = 0
        for line in clufr.readlines():
            curLine = line.split(',')
            if indexList[j] == curLine[0]:
                labelList.append(curLine[1])
            else:
                logging.error('indexList[' + str(j)+'] not equal' + curLine[0])
            j+=1
        return dataMat, labelList

    def loadDataFromDatabase(self):
        pwd = __file__
        qapair_vecfile = os.path.join(os.path.abspath(os.path.dirname(pwd) + os.path.sep + "../../"),
                                      "cluster/data/qapair_vec.txt")
        dataMat = []
        idList = []
        classLabelList = []
        qafr = open(qapair_vecfile)
        for line in qafr.readlines():
            curLine = line.strip().split(' ')
            idList.append(curLine[0])
            classLabelList.append(curLine[-1])
            curLine = curLine[1:-1]
            i = 0
            for s in curLine:
                curLine[i] = float(s)
                i += 1
            dataMat.append(curLine)

        return dataMat, classLabelList




    def trainNB(self):
        if self.dataMat is None:
            dataMat, labelList = self.loadDataFromDatabase()
            self.classifier.fit(dataMat, labelList)
        # self.saveModel()

    def predict(self, sentenceVec):
        return self.classifier.predict(sentenceVec)

    def saveModel(self):
        joblib.dump(self.classifier, '../model/clf.model')
        joblib.dump(self.dataMat, '../model/vec.model')
        joblib.dump(self.labelList, '../model/label.model')


if __name__ == '__main__':

    classifier = BayesClassifier()
    classifier.trainNB()
    pwd = __file__
    modelfile = os.path.join(os.path.abspath(os.path.dirname(pwd) + os.path.sep + "../../"),
                                  "word2vec/model/med250.model.bin")
    wordmodel = models.Word2Vec.load(modelfile)
    docmodel = Doc2Vec(wordmodel)
    senvec = mat(docmodel.query("聚类分析中常见的数据类型有哪些"))
    print(senvec)
    print(classifier.predict(senvec))
    pass