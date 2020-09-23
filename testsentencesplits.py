
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 17:33:27 2019

@author: Aashish
"""

import extraction.twitterHandle as th
import extraction.redditHandler as rh
import helpers.oauthConfigReader as ocr
import helpers.KeywordConfigsReader as kcr
from helpers.dbHelper import MongodbInteracter

from processing.preprocess import Preprocessor
from processing.sentenceSplitter.sentenceSplitter import splitSentence, splitSentenceVerbose
from processing.sentenceSplitter.coreferenceresolver import resolveCoreference
from processing.aspectsIdentifier import AspectIdentifier



# TODO: Add logic to switch between handle in a user friendly way. Read keys from config.      


if __name__ == '__main__':
    print('inside word split pipeline test')
    # set verbose to true for all debug
    verbose = True
    preprocessor = Preprocessor()
    dbHandle = MongodbInteracter(dbName='tsa', collectionName='tweets')
    tweets = dbHandle.fetchContents({})
    tweets = list(tweets)

    while True:
        print("\n"*4)
        print("input please: ", end="")
        x = input()
        x = preprocessor.clean(x)
        print("\nTweet text: ", x)
        # print("\n",classifier.classify(x))
        print("-"*100)
        if verbose:
            sents = splitSentenceVerbose(x)
        else:
            sents = splitSentence(x)
        

        resolveCoref= True
        print("before: ", sentence)
        if resolveCoref:
            sentence = resolveCoreference(sentence)
            print("\nafter coreference resolution: ", sentence)
        print("after coref")
        lst = sentenceSplitter_(sentence)
        print("\nafter sentence splitting: ", lst)

        simplifier = Simplifier()
        lst = simplifier.getSplitSentences(lst)
        print("\nafter simplifier: ", lst)
        
        lst = listOperation(lst, butGroupSplitter)
        print("\nafter butGroup splitting: ", lst)
        lst = listOperation(lst, eitherOrGroupSplitter)
        print("\nafter eitherorGroup splitting: ", lst)
        lst = listOperation(lst, conjunctionSplitter)
        print("\nafter conjunction splitting: ", lst)













