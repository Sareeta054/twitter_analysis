'''
    author: Bipin Oli
'''

from processing.aspectsIdentifier import AspectIdentifier
from processing.sentenceSplitter.sentenceSplitter import SentenceSplitter
from helpers.modelConfigReader import ModelConfigReader
from classify.naiveBayesClassifier import NaiveBayesClassifier
from helpers.modelInitializer import ModelInitializer
from classify.bertClassifier import BERTClassifier
from helpers.bertInteractor import BertInteractor
import os
import sys
import json


if __name__ == "__main__":
    project_root_path = os.path.split(
        os.path.dirname(os.path.realpath(__file__)))[0]
    sys.path.insert(0, project_root_path)


class Classifier:

    def __init__(self):
        self.aspectIdentifier = AspectIdentifier()
        self.selClassifier = ModelConfigReader.getSelectedClassifier()
        self.splitter = SentenceSplitter()

        availClassifiers = ModelConfigReader.getAvailableClassifiers()
        if self.selClassifier not in availClassifiers:
            print("\n---- ERROR: Error in modelConfigs.yml, {} not in model_saved_names\n".format(self.selClassifier))

        if self.selClassifier == "NaiveBayes":
            self.classifier = NaiveBayesClassifier("NaiveBayes")
            self.remoteClassifierModel = False
        elif self.selClassifier == "BERT":
            try:
                if (BertInteractor()).ping():
                    print("\n ---- Using BERT server ----\n")
                    self.classifier = BertInteractor()
                    self.remoteClassifierModel = True
                else:
                    print("\n<==***Model Server Not Ready***==>\n")
                    print("\n --- using new BERT instance ---\n")
                    self.classifier = ModelInitializer._getClassifier()
                    self.remoteClassifierModel = False            
            except Exception as e:
                print("\n<==***Model Server Error***==>\n", e)
                print("\n --- using new BERT instance ---\n")
                self.classifier = ModelInitializer._getClassifier()
                self.remoteClassifierModel = False            


    def classify(self, sentence, verbose=False):
        '''
        classify the sentence and return the classification in the detailed format like:
         {  
             "sentence": "Tweet text will be here.",
             "wo_split": { "result" : "neg", "pos" : 0.25, "neg" : 0.75 },
             "aspect_wise_prediction": { 
                 "jobs": { "result" : "neg", "pos" : 0.75, "neg" : 0.25 },
                 "immigration": { "result" : "neutral", "pos" : 0.5, "neg" : 0.5 },
             }
         }
        '''
        # if there are less than 2 aspects no need to split the sentence
        aspects = self.aspectIdentifier.identify(sentence)
        if len(aspects) > 1:
            sentence_wise_prediction, predictions = self._classifySentenceSplits(sentence, verbose)
            with_split = self._averagePrediction(predictions)
        else:
            result = self._classifyWithoutSentenceSplits(sentence)
            sentence_wise_prediction = [{"splitted_sentence": sentence, "pos": result['pos'], "neg": result['neg']}]
            with_split = {}
            for aspect in aspects:
                with_split[aspect] = result
        wo_split = self._classifyWithoutSentenceSplits(sentence)

        return {
            "sentence": sentence_wise_prediction,
            "wo_split": wo_split,
            "aspect_wise_prediction": with_split
        }

    def _classifySentenceSplits(self, sentence, verbose=True):
        '''
        Aspect based classification of the sentence
        by splittting it into multiple subsentences
        '''
        sents = self.splitter.splitSentenceVerbose(sentence)
        print(sents)
        if verbose:
            sents = self.splitter.splitSentenceVerbose(sentence)
            print(sents)
            print("\n\n--+++ original sentence: ", sentence)
            print("--++: splitted into: ")
            for sent in sents:
                print("------: ", sent)
        else:
            sents = self.splitter.splitSentence(sentence)

        # classify each sentence
        # identify aspects in each sentence
        # collect aspect wise classification of each sentence
        prediction = {}
        sentence_wise_prediction = []
        for sent in sents:
            print("------: ", sent)
            asps = self.aspectIdentifier.identify(str(sent))
            print(asps)
            result = self.classifier.classify(str(sent))
            res = json.loads(result) if self.remoteClassifierModel else result
            print(res)
            # print(res['input_text'])
            pred = {"splitted_sentence": sent, "pos": res['pos'], "neg": res['neg']}
            sentence_wise_prediction.append(pred)
            if verbose:
                print("----: ", sent, ": ", pred)
                print("----aspects: ", asps, "\n")
            for asp in asps:
                if asp not in prediction:
                    prediction[asp] = []
                prediction[asp].append(pred)
        return sentence_wise_prediction, prediction

    def _averagePrediction(self, prediction):
        '''
        averages the probabilities of the aspect
        '''
        retval = {}
        for aspect in prediction:
            poss = list(map(lambda x: x['pos'], prediction[aspect]))
            negs = list(map(lambda x: x['neg'], prediction[aspect]))
            pos_avg = sum(poss) / len(poss)
            neg_avg = sum(negs) / len(negs)
            pos = pos_avg / (pos_avg + neg_avg)
            neg = neg_avg / (pos_avg + neg_avg)
            thold = ModelConfigReader.getClassificationThreshold()
            result = "neutral"
            if pos >= thold:
                result = "pos"
            if neg >= thold:
                result = "neg"
            retval[aspect] = {"result": result, "pos": pos, "neg": neg}
        return retval

    def _classifyWithoutSentenceSplits(self, sentence):
        result = self.classifier.classify(str(sentence))
        # print("remote classifier model value =>{}".format(self.remoteClassifierModel))
        pred = json.loads(result) if self.remoteClassifierModel else result
        thold = ModelConfigReader.getClassificationThreshold()
        result = "neutral"
        if pred['pos'] >= thold:
            result = "pos"
        if pred['neg'] >= thold:
            result = "neg"
        return {"result": result, "pos": pred['pos'], "neg": pred['neg']}


# ---------- Testing ----------------------
if __name__ == "__main__":
    classifier = Classifier()
    sentence = "What a fascinating day. I am sure loving the weather."
    sentence2 = "I don't like this at all. Rich people dominating the value of democracy."
    print(classifier.classify(sentence))
    print(classifier.classify(sentence2))
