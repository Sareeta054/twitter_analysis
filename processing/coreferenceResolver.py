'''
    author: Bipin Oli
'''

from processing.spacySingleton import SpacyProvider

def resolveCoreference(sentence):
    nlp = SpacyProvider.getInstance()
    doc = nlp(sentence)
    return doc._.coref_resolved
