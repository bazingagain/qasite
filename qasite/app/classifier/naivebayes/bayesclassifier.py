# Created by leon at 12/12/2017

import logging

from numpy import *
from sklearn.naive_bayes import GaussianNB
from sklearn.externals import joblib
from qasite import settings
from qasite.app.word2vec.bean.doc2vec import Doc2Vec
import pathlib
import mysql.connector

class BayesClassifier:
    NAIVEBAYES_CLASSIFIER_FILE_PATH = settings.BASE_DIR + '/data/model/bayes/clf.model'
    DATAMAT_FILE_PATH = settings.BASE_DIR + '/data/model/bayes/vec.model'
    LABELLIST_FILE_PATH = settings.BASE_DIR + '/data/model/bayes/label.model'

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

    def loadDataFromModelFile(self):
        """
        从向量模型文件（由问答对训练集训练得到）中训练好的分类矩阵和类别标签
        :return:
        """
        dataMat,idList,classLabelList = [[], [], []]
        qafr = open(settings.QAPAIR_VEC_FILE)
        for line in qafr.readlines():
            curLine = line.strip().split(' ')
            idList.append(curLine[0])
            classLabelList.append(curLine[-1])
            curLine = list(map(float, curLine[1:-1]))
            dataMat.append(curLine)
        return dataMat, classLabelList

    def trainOrLoadNB(self):
        if self.modelFileExist():
            self.loadModel()
        else:
            self.dataMat, self.labelList = self.loadDataFromModelFile()
            self.classifier.fit(self.dataMat, self.labelList)
            self.saveModel()

    def predict(self, sentenceVec):
        return self.classifier.predict(sentenceVec)

    def saveModel(self):
        joblib.dump(self.classifier, self.NAIVEBAYES_CLASSIFIER_FILE_PATH)
        joblib.dump(self.dataMat, self.DATAMAT_FILE_PATH)
        joblib.dump(self.labelList, self.LABELLIST_FILE_PATH)

    def loadModel(self):
        self.classifier = joblib.load(self.NAIVEBAYES_CLASSIFIER_FILE_PATH)
        self.dataMat = joblib.load(self.DATAMAT_FILE_PATH)
        self.labelList = joblib.load(self.LABELLIST_FILE_PATH)

    @staticmethod
    def modelFileExist():
        if pathlib.Path(BayesClassifier.NAIVEBAYES_CLASSIFIER_FILE_PATH).exists() and \
            pathlib.Path(BayesClassifier.DATAMAT_FILE_PATH).exists() and \
                pathlib.Path(BayesClassifier.LABELLIST_FILE_PATH).exists():
            return True
        return False

def testQuestionClassify():
    classifier = BayesClassifier()
    classifier.trainOrLoadNB()
    docmodel = Doc2Vec(None)
    with open(settings.BASE_DIR + '/data/test/question.txt', 'r') as f:
        i = 0
        j = 0
        for line in f.readlines():
            j+=1
            senvec = mat(docmodel.query(line))
            classLabel = classifier.predict(senvec)[0]
            print(classLabel)
            if classLabel == '聚类分析':
                i+=1
        print(str(j) + "  " + str(i))


def testNoAnswerQuestionClassify():
    classifier = BayesClassifier()
    classifier.trainOrLoadNB()
    docmodel = Doc2Vec(None)
    con = mysql.connector.connect(user='root', password='root', database='test')
    cursor = con.cursor()
    cursor.execute('select * from qa_qapair')
    values = cursor.fetchall()
    dic = {}
    for v in values:
        question = v[1]
        classLabel = v[8]
        senvec = mat(docmodel.query(question))
        if classifier.predict(senvec)[0] == classLabel:
            if classLabel in dic.keys():
                dic[classLabel]['sum'] += 1
                dic[classLabel]['correct'] += 1
            else:
                dic[classLabel] = {'sum': 1, 'correct': 1, 'rate': 0}
        else:
            if classLabel in dic.keys():
                dic[classLabel]['sum'] +=1
            else:
                dic[classLabel] = {'sum':1, 'correct':0,'rate':0}
    for k in dic:
        dic[k]['rate'] = round(dic[k]['correct'] / dic[k]['sum'], 2)

    print(dic)

if __name__ == '__main__':
    pass