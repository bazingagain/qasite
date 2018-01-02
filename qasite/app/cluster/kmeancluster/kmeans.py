# Created by leon at 09/12/2017

from numpy import *
import matplotlib.pyplot as plt
import queue
import threading
import logging
from multiprocessing.pool import ThreadPool

def loadDataSet(fileName):
    """
    加载数据集

    每行: index 0.1223 0.13456 ...
    其中index为问答对在数据库中的id
    :param fileName: 输入数据文件名
    :return: 问题矩阵,索引列表
    """
    dataMat = []
    indexList = []
    fr = open(fileName)
    for line in fr.readlines():
        curLine = line.strip().split(' ')
        indexList.append(curLine[0])
        curLine = curLine[1:-1]
        # fltLine = map(float, curLine)  # map all elements to float()
        i = 0
        for s in curLine:
            curLine[i] = float(s)
            i+=1
        dataMat.append(curLine)
    return dataMat, indexList


def distEclud(vecA, vecB):
    return sqrt(sum(power(vecA - vecB, 2)))  # 计算欧式距离

def randCent(dataSet, k):
    n = shape(dataSet)[1]
    centroids = mat(zeros((k, n)))  # k 行,n列  随机创建k个初始簇心
    for j in range(n):  # create random cluster centers, within bounds of each dimension
        minJ = min(dataSet[:, j])
        rangeJ = float(max(dataSet[:, j])-minJ)
        centroids[:, j] = mat(minJ + rangeJ * random.rand(k, 1))
    return centroids


def kMeans(dataSet, k, distMeas=distEclud, createCent=randCent):
    m = shape(dataSet)[0] # 数据点数目
    clusterAssment = mat(zeros((m, 2)))
    centroids = createCent(dataSet, k) # 得到随机创建的簇心, k行,n列
    clusterChanged = True
    while clusterChanged:
        clusterChanged = False
        for i in range(m):  # 将每一个数据点分配到距离改点最近的质心
            minDist = inf
            minIndex = -1
            for j in range(k):
                distJI = distMeas(centroids[j, :], dataSet[i, :]) # 计算点到每个簇心的距离,找到最小距离的簇心的index
                if distJI < minDist:
                    minDist = distJI
                    minIndex = j
            if clusterAssment[i, 0] != minIndex: clusterChanged = True
            clusterAssment[i, :] = minIndex, minDist ** 2 # 第i个数据对应属于某个索引的簇心
        for cent in range(k):  # recalculate centroids
            ptsInClust = dataSet[nonzero(clusterAssment[:, 0].A == cent)[0]]  # get all the point in this cluster
            centroids[cent, :] = mean(ptsInClust, axis=0)  # 按列方向相加,并求平均值
    return centroids, clusterAssment

def biKmeans(dataSet, k, distMeas=distEclud):
    m = shape(dataSet)[0]
    clusterAssment = mat(zeros((m, 2))) # m行2列，其中第一列存放质心的索引，第2列存放误差平方和(SSE)
    centroid0 = mean(dataSet, axis=0).tolist()[0]
    centList = [centroid0]  # 计算所有点的唯一质心
    for j in range(m):  #  计算每个点的初始误差
        clusterAssment[j, 1] = distMeas(mat(centroid0), dataSet[j, :]) ** 2
    while (len(centList) < k):
        logging.info('centList.length is:' + str(len(centList)))
        lowestSSE = inf
        for i in range(len(centList)):
            ptsInCurrCluster = dataSet[nonzero(clusterAssment[:, 0].A == i)[0],:]  #获取第i个簇的数据点集合
            centroidMat, splitClustAss = kMeans(ptsInCurrCluster, 2, distMeas) # 对第i个簇进行2-Means聚类
            sseSplit = sum(splitClustAss[:, 1])  # 第i簇进行2-Means后的总误差
            sseNotSplit = sum(clusterAssment[nonzero(clusterAssment[:, 0].A != i)[0], 1]) # 其它簇的总误差
            if (sseSplit + sseNotSplit) < lowestSSE:  # 进行二分后的总误差与当前总误差比较
                bestCentToSplit = i
                bestNewCents = centroidMat
                bestClustAss = splitClustAss.copy()
                lowestSSE = sseSplit + sseNotSplit
        bestClustAss[nonzero(bestClustAss[:, 0].A == 1)[0], 0] = len(centList)  # 划分到第 len(centList) 新簇
        bestClustAss[nonzero(bestClustAss[:, 0].A == 0)[0], 0] = bestCentToSplit # 划分到原第bestCentToSplit簇
        centList[bestCentToSplit] = bestNewCents[0, :].tolist()[0]  # 将原来的簇心以两个新的簇心进行替代
        centList.append(bestNewCents[1, :].tolist()[0])
        clusterAssment[nonzero(clusterAssment[:, 0].A == bestCentToSplit)[0],:] = bestClustAss  # reassign new clusters, and SSE
    return mat(centList), clusterAssment

def testGoodK(k, q):
    logging.info('clas test GoodK')
    datMat4, indexList = loadDataSet('../data/qapair_vec.txt')
    datMat4 = mat(datMat4)
    centerList, myNewAssments=biKmeans(datMat4, k)
    print(str(k) + ":" + str(shape(centerList)) + ":" + str(sum(myNewAssments[:,1])))
    q.put(sum(myNewAssments[:,1]))

def show():
    k = range()
    pool = ThreadPool(processes=5)
    qs = []
    errrate = []
    for i in k:
        q = queue.Queue()
        pool.apply_async(testGoodK, args=(i, q))
        qs.append(q)
    for q in qs:
        price = q.get()
        errrate.append(price)
    plt.plot(k, errrate, 'o', label='data')
    plt.xlabel('input k')
    plt.ylabel('error Assement')
    plt.xlim([30, 50])
    plt.ylim([0, 20])
    plt.title('bisecting K-means')
    plt.grid()
    plt.legend(loc=2)
    plt.show()

def getClusterWithSingle(k):
    # TODO 做出线程启动方式
    logging.info('test getClusterWithSingle')
    datMat4, indexList = loadDataSet('../data/qapair_vec.txt')
    datMat4 = mat(datMat4)
    centerList, myNewAssments = biKmeans(datMat4, k)
    print(str(k) + ":" + str(shape(centerList)) + ":" + str(sum(myNewAssments[:, 1])))
    output = open('../data/clusterindex_'+str(k)+'.txt', 'w')
    for i in range(len(indexList)):
        output.write(str(indexList[i]) + "," + str(myNewAssments[i,0]))
        output.write('\n')
    output.close()
    print(sum(myNewAssments[:, 1]))

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    getClusterWithSingle(8)
    # show()