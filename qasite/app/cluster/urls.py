# Created by leon at 14/12/2017

from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^trainqapairvec$', views.trainqapairvec, name='trainqapairvec'),
]
