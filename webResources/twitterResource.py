from helpers.dbHelper import MongodbInteracter
from flask_restful import Resource, request

class TwitterCountResource(Resource):

    def get(self):
        queryParams = request.args
        paramCheck = paramChecker(queryParams)
        if not paramCheck:
            return "Invalid URL/Params.", 400
        else:
            db = MongodbInteracter(dbName='tsa', collectionName='tweets')
            pipeline = [{'$match' : {'keyword' : {'$regex' : queryParams['name'], '$options': 'im'}}},
                {'$group' : {'_id' : '$keyword', 'count' : {'$sum' : 1}}}]
            return db.aggregation(pipeline=pipeline), 200

class TwitterDataResource(Resource):
    def get(self):
        queryParams = request.args
        paramCheck = paramChecker(queryParams)
        if not paramCheck:
            return "Invalid URL/Params.", 400
        else:
            db = MongodbInteracter(dbName='tsa', collectionName='tweets')
            return db.fetchContentsViaKeyword(keyword=queryParams['name']), 200

def paramChecker(queryParams):
    return (False if list(filter(lambda x: not (x == 'name' or x =='date'), queryParams.keys())) else True) and ('name' in queryParams.keys())