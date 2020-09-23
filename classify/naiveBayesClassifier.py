'''
    author: Bipin Oli
'''

import pickle 
import os, sys
from nltk import classify
from nltk import NaiveBayesClassifier



if __name__ == "__main__":
    project_root_path = os.path.split(os.path.dirname(os.path.realpath(__file__)))[0]
    sys.path.insert(0, project_root_path)
    
    

from helpers.modelConfigReader import ModelConfigReader
from processing.tweetCleanerNaivesBayes import bagOfWords



class NaiveBayesClassifier:

    def __init__(self, model_name="NaiveBayes"):
        model_path = os.path.join(os.path.split(os.path.realpath(__file__))[0],ModelConfigReader.getModelFolder(), ModelConfigReader.getModelSavedName(model_name))
        print("model path: " + model_path)
        self.classifier = pickle.load(open(model_path, "rb"))


    def _mostInformativeFeatures(self, limit=20):
        return self.classifier.show_most_informative_features(limit)


    def classify(self, sentence):
        '''
        classify the sentence into postive or negative.
        It returns classification with probability values.
        for eg: {'prediction': 'pos', 'pos': 0.582766958567508, 'neg': 0.41723304143249396}
        '''
        probResult = self.classifier.prob_classify(bagOfWords(sentence))
        return {
            "prediction": probResult.max(),
            "pos": probResult.prob("pos"),
            "neg": probResult.prob("neg")
        }




# ---------- Testing ----------------------
if __name__ == "__main__":
    classifier = NaiveBayesClassifier()
    sentence = "What a fascinating day. I am sure loving the weather."
    sentence2 = "I don't like this at all. Rich people dominating the value of democracy."
    print(classifier.classify(sentence))
    print(classifier.classify(sentence2))
