# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 17:15:19 2019

@author: Aashish
"""
from bson.json_util import dumps
import json
from helpers.dbHelper import MongodbInteracter
from flask_restful import Resource, request
from helpers.dbHelper import DatabaseConfigReader
from classify.classifier import Classifier

class ClassificationPipelineResource(Resource):

    def get(self):
        # queryParams = request.args
        # paramCheck = paramChecker(queryParams)
        paramCheck = True
        if not paramCheck:
            return "Invalid URL/Params.", 400
        else:
            self.db = MongodbInteracter(dbName='tsa', collectionName='tweets')
            self.classifier = Classifier()
            try:
                result = self.runPipeLine()
                # print("\n,<==RESULT==>\n", result)
                return json.loads(dumps(result)), 200
            except Exception as e:
                print("\n<==***Error In Classification Pipeline***==>\n", e)
                return "ERROR: Classification Pipeline encountered error. View Log for details", 500

    def runPipeLine(self):
        fetchedTweets = list(self.db.fetchContentsViaKeyword('amy'))
        return [self.classifier.classify(x['tweetText']) for x in fetchedTweets[0:100]]
        

def paramChecker(queryParams):
    return (False if list(filter(lambda x: not (x == 'media'), queryParams.keys())) else True) and ('media' in queryParams.keys())
