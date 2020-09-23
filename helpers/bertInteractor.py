import os, sys
import requests

from helpers.modelConfigReader import ModelConfigReader

class BertInteractor:
    def __init__(self):
        self.url = ModelConfigReader.getModelServerURL()
    
    def classify(self, sentence):
        x = {'payload': sentence}
        return (requests.post(self.url, json=x)).text

    def ping(self):
        retStatus = requests.get(self.url)
        return retStatus.status_code == 200

