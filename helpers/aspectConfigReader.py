'''
    author: Bipin Oli
'''

import helpers.genericConfigReader as gcr

# TODO: there has be lot of code duplication
# needs refactoring
class AspectConfigReader:
    @staticmethod
    def getAspects():
        reader = gcr.ConfigReader()
        reader.readConfigFile("aspectConfigs.yml", "aspects")
        configs = reader.getConfigs()
        return configs

    @staticmethod
    def getCachePath():
        reader = gcr.ConfigReader()
        reader.readConfigFile("aspectConfigs.yml", "related_words_cache")
        configs = reader.getConfigs()
        return configs

    @staticmethod
    def getCacheTimeout():
        reader = gcr.ConfigReader()
        reader.readConfigFile("aspectConfigs.yml", "cache_time_out")
        configs = reader.getConfigs()
        return configs

    @staticmethod
    def getJsonPath():
        reader = gcr.ConfigReader()
        reader.readConfigFile("aspectConfigs.yml", "related_words_json")
        configs = reader.getConfigs()
        return configs

    @staticmethod
    def isStatic():
        reader = gcr.ConfigReader()
        reader.readConfigFile("aspectConfigs.yml", "related_words")
        staticStatus = reader.getConfigs()

        if staticStatus == "Dynamic":
            return False 
        return True