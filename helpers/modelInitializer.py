import spacy
from classify.bertClassifier import BERTClassifier

class ModelInitializer :

    nlp = {}
    classifier = None

    @classmethod
    def _getClassifier(cls):
        if cls.classifier is None:
            cls.classifier = BERTClassifier()
        return cls.classifier

    @classmethod
    def _getNlpModel(cls, model):
        if not cls.nlp or model not in cls.nlp.keys() :
            cls.nlp[model] = spacy.load(model)
        return cls.nlp[model]