from django.shortcuts import render
from django.shortcuts import HttpResponse
import os
from gensim import models
from qasite.app.word2vec.docvecmodel import Doc2Vec
from qasite.app.cluster.kmeancluster import kmeans
from qasite.app.qa.models import QAPair,UserQAPair
import logging

def index(requset):
    pass

def trainqapairvec(request):
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    pwd = __file__
    word2vecmodelpath = os.path.join(os.path.abspath(os.path.dirname(pwd)+os.path.sep+".."), "word2vec/model/med250.model.bin")
    qavecpath = os.path.join(os.path.abspath(os.path.dirname(pwd)+os.path.sep+"."), "data/qapair_vec.txt")
    wordmodel = models.Word2Vec.load(word2vecmodelpath)
    docmodel = Doc2Vec(wordmodel)
    output = open(qavecpath, 'w')
    i = 0
    for e in QAPair.objects.all():
        vec = docmodel.query(e.question)
        if vec is None:
            logging.info(str(e.id) + ' ' + e.question)
            # e.delete()
        else:
            i+=1
            output.write(str(e.id))
            for v in vec:
                output.write(' ' + str(v))
            output.write(' ' + e.classLabel)
            output.write('\n')
    output.close()
    return HttpResponse(str(i) + '条记录')

def cluster(request):
    k = 8
    kmeans.getClusterWithSingle((8))


