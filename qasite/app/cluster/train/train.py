# Created by leon at 11/12/2017
from gensim import models
from qasite.app.word2vec.docvecmodel import Doc2Vec
from qasite.app.cluster.kmeancluster import kmeans
from qasite.app.qa.models import QAPair,UserQAPair
import logging
import os,django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "qasite.settings")
django.setup()



def prepare():
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    wordmodel = models.Word2Vec.load('../../word2vec/model/med250.model.bin')
    docmodel = Doc2Vec(wordmodel)
    output = open('../data/qapair_vec.txt', 'w')
    i = 0
    for e in QAPair.objects.all():
        i+=1
        vec = docmodel.query(e.question)
        output.write(e.id + ' ' + vec)
        output.newlines()
        if i > 10:
            break
    output.close()

if __name__ == '__main__':
    prepare()








