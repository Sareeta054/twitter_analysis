# -*- coding: utf-8 -*-
"""
Created on Wed Nov 13 11:26:38 2019

@author: alok.regmi
"""
import os
import ktrain
import numpy as np
import sys

from helpers.modelConfigReader import ModelConfigReader

if __name__ == "__main__":
    project_root_path = os.path.split(
        os.path.dirname(os.path.realpath(__file__)))[0]
    sys.path.insert(0, project_root_path)

class BERTClassifier:

    def __init__(self, remote_url=None, model_name="BERT"):
        self.remote_url = remote_url
        self.classification_classes = ["neg", "pos"]
        self.results = {}
        self.local_url = os.path.join(os.path.split(os.path.realpath(__file__))[
                                      0], ModelConfigReader.getModelFolder())
        self.model_name = ModelConfigReader.getModelSavedName(model_name)
        self.model = self._loadModel()

    def _saveModel(self):
        self.model.save(self.local_url)
        print("Model saved locally to disk")

    def _loadModel(self):
        if(not self.local_url):
            model = ktrain.load_predictor(self.remote_url)
        else:
            model = ktrain.load_predictor(
                os.path.join(self.local_url, self.model_name))
        print("--load model: ", model)
        return model

    def classify(self, text):
        predictions = self.model.predict(text, return_proba=True)
        print("The predictions array is :")
        print(predictions)
        print("-------------------------------------------------")
        pred_class = np.argmax(predictions)
        return {
            "input_text": text,
            "prediction": self.classification_classes[pred_class],
            "pos": predictions[1].item(),
            "neg": predictions[0].item()
        }

if __name__ == "__main__":
    classifier = BERTClassifier()
    sentence = "What a fascinating day. I am sure loving the weather."
    sentence2 = "I don't like this at all. Rich people dominating the value of democracy."
    print(classifier.classify(sentence))
    print(classifier.classify(sentence2))