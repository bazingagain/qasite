# Created by leon at 14/12/2017

from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^appraise$', views.appraise, name='appraise'),
    url(r'^train$', views.train, name='train'),
    url(r'^ask$', views.ask, name='ask'),
    url(r'^asktest$', views.asktest, name='asktest'),
]
