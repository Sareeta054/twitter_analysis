# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 16:14:25 2019

@author: Aashish
"""
import helpers.genericConfigReader as gcr

class OauthConfigsReader:
    @staticmethod
    def getTwitterConfigs():
        reader = gcr.ConfigReader()
        reader.readConfigFile('OauthConfigs.yml','twitter')
        configs = reader.getConfigs()
        return configs
    
    @staticmethod
    def getRedditConfigs():
        reader = gcr.ConfigReader()
        reader.readConfigFile('OauthConfigs.yml','reddit')
        configs = reader.getConfigs()
        return configs
    
    