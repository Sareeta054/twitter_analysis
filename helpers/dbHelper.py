# pylint: disable=E1136
# [Disables certain Lynt warning]
# -*- coding: utf-8 -*-
"""
@author: Aashish

Description: Helper class for mongodb CRUD operations
"""

import pymongo
from bson.json_util import dumps
import json
from helpers.dbConfigReader import DatabaseConfigReader


class MongodbInteracter:
    
    """ TODO: Research on upsert vs insert for large data.
              MongoDb security and Auth.
    """
    __dbClient = None

    #Connects Database [Singleton Pattern to ensure a single instance]
    @classmethod
    def __connectDatabase(cls, dbHost, dbPort, username=None, password=None , authSource="admin", authMechanism=None,):
        if cls.__dbClient is None:
            try:
                cls.__dbClient = pymongo.MongoClient(host=dbHost, port=dbPort, username=username,password=password, authSource=authSource, authMechanism=authMechanism)
            except Exception as e:
                print("\n<==***Db Connection Error==>***\n", e)
            else:
                print("\n<==***Db Connection Successful***==>\n", cls.__dbClient)

    
    def __init__(self, dbName=None, collectionName=None):
        dbConfigs = DatabaseConfigReader.getDbInformationConfigs()
        dbAuthConfigs = DatabaseConfigReader.getDbAuthenticationConfigs()
        self.dbName = dbConfigs['dbName'] if dbName is None else dbName
        self.collectionName = dbConfigs['collections'][collectionName] if collectionName is not None else dbConfigs['collections']['twitter']
        self.__connectDatabase(dbConfigs['dbHost'],dbConfigs['dbPort'],
                username=dbAuthConfigs['user'],
                password=dbAuthConfigs['pwd'], authSource=dbAuthConfigs['authSource'],
                authMechanism=dbAuthConfigs['authMechanism'])

    #For posting single object to database.
    def postContent(self, content):
        try:
            cursor = self.__dbClient[self.dbName][self.collectionName].update_one({'_id' : {'$eq' : content['_id']}}, content, upsert=True)
        except Exception as e:
            print("\n<==***Post Error***==>\n", e)
        else:
            print("\n<==***Post Result***==>\n", cursor.raw_result)

    #For posting single object to database.
    def replaceOnce(self, content):
        try:
            cursor = self.__dbClient[self.dbName][self.collectionName].replace_one({'_id' : {'$eq' : content['_id']}}, content, upsert=True)
        except Exception as e:
            print("\n<==***Post Error***==>\n", e)
        else:
            print("\n<==***Post Result***==>\n", cursor.raw_result)

    #For posting list of objects to database.
    def postContents(self, contents):
        try:
            operations = [pymongo.UpdateOne({'_id' : {'$eq' : content['_id']}}, {'$set' : content}, upsert=True) for content in contents]
            cursor = self.__dbClient[self.dbName][self.collectionName].bulk_write(operations)
        except Exception as e:
            print("\n<==***Bulk Post Error***==>\n", e)
        else:
            print("\n<==***Bulk Post Result***==>\n", cursor.bulk_api_result)

    #Fetch Contents Via a custom query(what to search) and projection(how to view result) param. [See Mongo Docs for More Info.]
    def fetchContents(self, query={}, projection=None):       
        try:
            return json.loads(dumps(self.__dbClient[self.dbName][self.collectionName].find(query, projection)))
        except Exception as e:
            print("\n<==***Fetch Error***==>\n", e)

    #Aggregation function via custom pipeline.
    def aggregation(self, pipeline=None):
        try:
            return json.loads(dumps(self.__dbClient[self.dbName][self.collectionName].aggregate(pipeline)))
        except Exception as e:
            print("\n<==***Aggregation Error***==>\n", e)

    #Fetch contents based on keyword.
    def fetchContentsViaKeyword(self, keyword=""):
        query = {'keyword' : {'$regex' : keyword, '$options': 'im'}}
        return self.fetchContents(query=query)