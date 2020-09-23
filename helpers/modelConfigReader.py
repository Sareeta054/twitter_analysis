'''
    author: Bipin
'''

import helpers.genericConfigReader as gcr

class ModelConfigReader:
    configFile = "modelConfigs.yml"
    reader = gcr.ConfigReader()

    @staticmethod
    def getModelFolder():
        ModelConfigReader.reader.readConfigFile(ModelConfigReader.configFile, "models_folder")
        configs = ModelConfigReader.reader.getConfigs()
        return configs

    @staticmethod
    def getSelectedClassifier():
        ModelConfigReader.reader.readConfigFile(ModelConfigReader.configFile, "selected_classifier")
        configs = ModelConfigReader.reader.getConfigs()
        return configs
    
    @staticmethod
    def getAvailableClassifiers():
        ModelConfigReader.reader.readConfigFile(ModelConfigReader.configFile, "available_classifiers")
        configs = ModelConfigReader.reader.getConfigs()
        return configs

    @staticmethod
    def getModelSavedName(model):
        ModelConfigReader.reader.readConfigFile(ModelConfigReader.configFile, "model_saved_names")
        configs = ModelConfigReader.reader.getConfigs()
        return configs[model]

    @staticmethod
    def getClassificationThreshold():
        ModelConfigReader.reader.readConfigFile(ModelConfigReader.configFile, "classification_threshold")
        configs = ModelConfigReader.reader.getConfigs()
        return configs
    
    @staticmethod
    def getModelServerURL():
        ModelConfigReader.reader.readConfigFile(ModelConfigReader.configFile, "model_server_url")
        configs = ModelConfigReader.reader.getConfigs()
        print("\n configs\n",configs)
        return str(configs)