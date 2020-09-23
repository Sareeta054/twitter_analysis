# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 14:39:19 2019

@author: Aashish
"""
import yaml
import os

class ConfigReader:
    def readConfigFile(self, filename, section = None):
        self.config_path = os.path.join(os.path.split(os.path.dirname(os.path.realpath(__file__)))[0] ,os.path.join('config', filename))
        self.section = section
        # print("Path: ", self.config_path)
    
    def getConfigs(self):
        with open(self.config_path, 'r') as openedConfig:
            configs = yaml.load(openedConfig, Loader=yaml.FullLoader)
            if self.section:
                return configs[self.section]
            else:
                return configs
                