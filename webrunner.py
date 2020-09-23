# -*- coding: utf-8 -*-
"""
@author: Aashish
"""
from apscheduler.schedulers.background import BackgroundScheduler
from webResources.formResource import FormResource
from webResources.pipelineResource import ClassificationPipelineResource
from webResources.twitterResource import TwitterCountResource, TwitterDataResource
from flask_restful import Api
from flask import Flask
from jobs import autoTweetExtraction, autoTweetClassification
import os
import sys
if __name__ == "__main__":
    project_root_path = os.path.split(
        os.path.dirname(os.path.realpath(__file__)))[0]
    sys.path.insert(0, project_root_path)

if __name__ == "__main__":
    app = Flask(__name__, template_folder='webFeatures')
    app.config['SECRET_KEY'] = 'Very Hard Key You Cant Guess'
    api = Api(app)
    api.add_resource(TwitterCountResource, "/tweet", endpoint='tweet_count')
    api.add_resource(TwitterDataResource, "/tweet/full",
                     endpoint='tweet_full_data')
    api.add_resource(ClassificationPipelineResource,
                     "/result/summerized", endpoint='summerized_result')
    api.add_resource(FormResource, "/textSplit", endpoint='test_pipeline')
    scheduler = BackgroundScheduler()
    dailyTweetFetch = autoTweetExtraction.AutoTweetExtraction()
    dailyTweetClassification = autoTweetClassification.AutoTweetClassifcation()
    fetchTask = scheduler.add_job(
        dailyTweetFetch.run, 'interval', minutes=24*60)
    fetchTask = scheduler.add_job(
        dailyTweetClassification.run, 'interval', minutes=24*60)
    scheduler.start()
    app.run(host='0.0.0.0', port=8080)
