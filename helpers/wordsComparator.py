'''
    author: Bipin
'''

from nltk.corpus import wordnet 
from nltk.stem import WordNetLemmatizer 
from nltk.stem import PorterStemmer 

import nltk

# Part of speech tagging
def getPosTags(sentence):
    return nltk.pos_tag(nltk.word_tokenize(sentence))


# synonyms of the given word
def synonyms(word):
    '''Synonyms of the given word'''
    retval = set()
    for syn in wordnet.synsets(word):
        for l in syn.lemmas():
            retval.add(l.name())
    return list(retval)


# antonyms of the given word
def antonyms(word):
    '''Antonyms of the given word'''
    retval = set()
    for syn in wordnet.synsets(word):
        for l in syn.lemmas():
            for antonym in l.antonyms():
                retval.add(antonym.name())
    return list(retval)


# similarity score between two words
def getSimilarity(word1, word2):
    '''Wu Palmer similarity measure between words.
       Range: (0,1]
       ouput of 1 means perfect matching so perfect similarity
    '''
    word1 = wordnet.synsets(word1)[0]
    word2 = wordnet.synsets(word2)[0]
    print("-- comparing {} and {}.".format(word1.name(), word2.name()))
    return word1.wup_similarity(word2)


def lemmatize(word):
    lemmatizer = WordNetLemmatizer() 
    word = lemmatizer.lemmatize(word)
    stemmer = PorterStemmer()
    return stemmer.stem(word)