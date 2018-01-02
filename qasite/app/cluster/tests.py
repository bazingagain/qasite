from django.test import TestCase
import logging
import os

def prepare(request):
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    pwd = os.getcwd()
    filepath = os.path.join(os.path.abspath(os.path.dirname(pwd)+os.path.sep+"."), "word2vec/model/med250.model.bin")
    print(filepath)

prepare(None)


