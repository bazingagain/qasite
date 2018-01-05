import django
import json
import logging
import os

from django.conf import settings
from django.core.cache import cache
from django.http import HttpResponse
from django.shortcuts import render
from gensim import models
from numpy import *
from qasite.app.classifier.naivebayes import bayesclassifier
from qasite.app.qa.models import QAPair,UserQAPair
from qasite.app.word2vec.bean.doc2vec import Doc2Vec

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "qasite.settings")
django.setup()

def resp(object, content_type = "application/json"):
    return HttpResponse(json.dumps(object), content_type=content_type)

def index(request):
    return render(request, 'qa/index.html')

def appraise(request):
    """
    用户对答案进行评价
    :param request:
    :return:
    """
    if request.POST:
        id = request.POST['id']
        level = request.POST['level']
        if id is None:return resp({'status':'error', 'msg':'id is None'})
        if level is None:return resp({'status':'error', 'msg':'level is None'})
        try:
            qapair = QAPair.objects.get(pk=int(id))
            qapair.value += int(level)
            qapair.save()
            return resp({'status': 'success'})
        except QAPair.DoesNotExist:
            return resp({'status':'error', 'msg':'no such q&a pair'})
    else:return resp({'status':'error', 'msg':'method is not POST'})

def train(request):
    """
    保持用户提交的问答对
    :param request:
    :return:
    """
    if request.POST:
        ask = request.POST['ask']
        answer = request.POST['answer']
        if ask is None:return resp({'status':'error', 'msg':'ask is None'})
        if answer is None:return resp({'status':'error', 'msg':'answer is None'})
        userQAPair = UserQAPair(question=ask, answer=answer)
        userQAPair.save()
        return resp({'status':'success'})
    else:return resp(resp({'status':'error', 'msg':'method is not POST'}))

def ask(request):
    """
    用户获取答案
    #Django模式 https://segmentfault.com/q/1010000004204037/a-1020000004205900
    :param request:
    :return:
    """
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    if request.method == 'GET':
        ask = request.GET.get('ask')
        if ask is None:return resp({'status':'error', 'answer':'ask is None'})
        classifier = cache.get('classifier')
        if classifier is None:
            classifier = bayesclassifier.BayesClassifier()
            classifier.trainOrLoadNB()
            cache.set('classifier', classifier)
        docmodel = cache.get('docmodel')
        if docmodel is None:
            docmodel = Doc2Vec(None)
            cache.set('docmodel', docmodel)
        vec = docmodel.query(ask)
        if vec is None:
            return resp({'status': 'success', 'answer': '不知道你在说什么', 'similarity': -1.0})
        # 1. 对问题进行分类,找到该问题属于哪个问题,通过朴素贝叶斯
        senvec = mat(vec)
        classLabel = classifier.predict(senvec)[0]
        logging.info(classLabel)
        entrys = QAPair.objects.filter(classLabel=classLabel)
        # 2. 从该分类中通过使用word2vec的模型,找到最相近的问题,并返回其答案
        boost = 0.5
        answer = None
        maxSimilarity = float(-1)
        for e in entrys:
            similarity = docmodel.similarity(e.question, ask)
            if similarity > boost:
                boost = similarity
                maxSimilarity = similarity
                answer = e.answer
        return resp({'status':'success', 'answer': answer, 'similarity': maxSimilarity})

        # 3. 若相似度小于某个阈值,则调用网络接口从搜索引擎请求数据,提取答案并排序,然后进行相似性计算


def asktest(request):
    if request.method == 'GET':
        ask = request.GET.get('ask')
        return resp({'status':'success', 'answer':'寻找答案中...'})
        if ask is None:return resp({'status':'error', 'msg':'ask is None'})





