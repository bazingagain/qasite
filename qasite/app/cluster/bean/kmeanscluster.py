# Created by leon at 03/01/2018
from sklearn.cluster import KMeans
from sklearn.externals import joblib
from qasite import settings
import numpy as np

class KMeansCluster():
    """
    KMeans 聚类, 对sklearn进行一层包装
    """

    MODEL_DIR = settings.BASE_DIR+'/data/model/kmeans/cluster.model'

    def __init__(self, X, n_cluster, random_state=0, saveModel=False):
        self.X = X
        self.n_cluster = n_cluster
        self.random_state = random_state
        self.kmeans = KMeans(n_clusters=n_cluster, random_state=random_state).fit(X)
        if saveModel:
            joblib.dump(self.kmeans, KMeansCluster.MODEL_DIR)

    def predict(self, data):
        return self.kmeans.predict(data)

    def getLabels(self):
        return self.kmeans.labels_

    def getClusterCenters(self):
        return self.kmeans.cluster_centers_

if __name__ == '__main__':
    dataMat = []
    indexList = []
    fr = open(settings.QAPAIR_VEC_FILE)
    for line in fr.readlines():
        curLine = line.strip().split(' ')
        indexList.append(curLine[0])
        curLine = curLine[1:-1]
        fltLine = list(map(float, curLine))
        dataMat.append(fltLine)
    dataMat = np.mat(dataMat)
    km = KMeansCluster(dataMat, 8, 0)
    print(km.getLabels())
    print(km.getClusterCenters())





