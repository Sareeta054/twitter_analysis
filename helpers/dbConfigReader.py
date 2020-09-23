import helpers.genericConfigReader as gcr

class DatabaseConfigReader:
    @staticmethod
    def getDbAuthenticationConfigs():
        reader = gcr.ConfigReader()
        reader.readConfigFile('dbConfigs.yml', 'authentication')
        configs = reader.getConfigs()
        return configs
    
    @staticmethod
    def getDbInformationConfigs():
        reader = gcr.ConfigReader()
        reader.readConfigFile('dbConfigs.yml','database')
        configs = reader.getConfigs()
        return configs