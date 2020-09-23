# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 17:33:27 2019

@author: Aashish
"""

import extraction.twitterHandle as th
import extraction.redditHandler as rh
from helpers.dbHelper import MongodbInteracter
import helpers.KeywordConfigsReader as kcr
from classify.classifier import Classifier
from processing.preprocess import Preprocessor
from helpers.dbVisualize import DataVisualizer

class Runner:
    def initTwitterHandle(self):
        self.tHandle = th.TwitterHandle()

    def initRedditHandler(self):
        self.rHandler = rh.RedditHandler()


# TODO: Add logic to switch between handle in a user friendly way. Read keys from config.
if __name__ == '__main__':
    print('inside main')
    runner = Runner()
    preprocessor = Preprocessor()
    classifier = Classifier()
    dataVisualizer = DataVisualizer()

    # For twitter
    runner.initTwitterHandle()
    runner.tHandle.authenticate()
    
    # runner.initRedditHandler()
    # runner.rHandler.fetchFromSubreddit("Politics")

    # get keywords to search from the config file
    kwConfigTwitter = kcr.KeywordConfigsReader.getTwitterKeywordConfigs()

    # twitter handle to search for Amy
    twitterHandle = kwConfigTwitter['handle'][0]


    # dbHandle = MongodbInteracter(dbName='tsa', collectionName='tweets')
    # tweets = dbHandle.fetchContents({})
    # tweets = list(tweets)

    # overall result visualization
    # dataVisualizer.visualizer()

    while True:
        print("\n"*4)
        print("input please: ", end="")
        x = input()
        print("\n"*1)
        x = preprocessor.clean(x)
        print("\Preprocessed text: ", x)
        # print("\n", classifier.classify(x))
        print("-"*100)
