
import helpers.genericConfigReader as gcr

class KeywordConfigsReader:
    @staticmethod
    def getTwitterKeywordConfigs():
        reader = gcr.ConfigReader()
        reader.readConfigFile('keywordConfigs.yml','twitter')
        configs = reader.getConfigs()
        return configs
    
    @staticmethod
    def getRedditKeywordConfigs():
        reader = gcr.ConfigReader()
        reader.readConfigFile('keywordConfigs.yml','reddit')
        configs = reader.getConfigs()
        return configs
    