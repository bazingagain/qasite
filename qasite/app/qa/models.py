from django.db import models
from django.utils import timezone

class QAPair(models.Model):
    """
    系统默认问答对
    """
    question = models.CharField(max_length=1000)
    answer = models.TextField()
    classLabel = models.CharField(max_length=100, default=None)
    type = models.CharField(max_length=100, default=None)
    value = models.IntegerField(default=0)
    cluster = models.IntegerField(default=-1)
    createDate = models.DateTimeField(name='create_date', default=timezone.now())
    modifiedDate = models.DateTimeField(name='modified_date', auto_now=True)


class UserQAPair(models.Model):
    """
    用户提交问答对
    """
    question = models.CharField(max_length=1000)
    answer = models.TextField()
    type = models.CharField(max_length=100)
    value = models.IntegerField()
    createDate = models.DateTimeField(name='create_date', default=timezone.now())
    modifiedDate = models.DateTimeField(name='modified_date', auto_now=True)