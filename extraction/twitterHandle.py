# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 10:05:19 2019

@author: Aashish
"""
import sys
import os
if __name__ == "__main__":
    project_root_path = os.path.split(
        os.path.dirname(os.path.realpath(__file__)))[0]
    sys.path.insert(0, project_root_path)
import tweepy
import pytz
import datetime
from dateutil import parser
from helpers.oauthConfigReader import OauthConfigsReader as ocr
from helpers.dbHelper import MongodbInteracter
# TODO: Refactor for better approach

class TwitterHandle:

    def __init__(self):
        print('inside twitter handler')
        authConfigs = ocr.getTwitterConfigs()
        self.consumer_key = authConfigs['consumer_key']
        self.consumer_secret = authConfigs['consumer_secret']
        self.access_key = authConfigs['access_key']
        self.access_secret = authConfigs['access_secret']
        self.tweets = []
        self.authenticate()

    def authenticate(self):
        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_key, self.access_secret)
        self.api = tweepy.API(auth, wait_on_rate_limit=True,
                              wait_on_rate_limit_notify=True)

    def searchByKeyword(self, keyword, until="", since="", count=None, result_type="recent"):
        """
        Implementing method of cursors to implement collection of tweets properly
        No count means get all the tweets that match the criteria
        """
        if count is None:
            tweets = tweepy.Cursor(self.api.search, q=keyword, until=until, since=since, result_type=result_type,
                                   full_text=True, tweet_mode="extended", lang="en").items()
        else:
            tweets = tweepy.Cursor(self.api.search, q=keyword, until=until, since=since, result_type=result_type,
                                   full_text=True, tweet_mode="extended", lang="en").items(count)

        for status in tweets:
            createdDate = parser.parse(str(status._json["created_at"]).strip())
            createdDate = createdDate.replace(
                tzinfo=pytz.utc) - createdDate.utcoffset()
            status_refined = {
                'keyword': keyword,
                '_id': status._json["id"],
                'created_at': createdDate,
                'tweetText': status._json["full_text"],
                'hashtags': status._json["entities"]["hashtags"],
                'userLoc': status._json["user"]["location"],
                'tweetGeo': status._json["geo"],
                'tweetCoordinates': status._json["coordinates"],
                'tweetPlace': status._json["place"],
                'retweet': {},
            }
            if hasattr(status, "retweeted_status"):
                status_refined['tweetText'] = status._json["retweeted_status"]["full_text"]
                status_refined['retweet'] = {
                    'original_retweet_id': status._json["retweeted_status"]["id"],
                    'origUserLoc': status._json["retweeted_status"]["user"]["location"],
                    'origTweetLoc': status._json["retweeted_status"]["geo"],
                    'origTweetPlace': status._json["retweeted_status"]["place"],
                    'origTweetCoord': status._json["retweeted_status"]["coordinates"],
                    'origHashtags': status._json["retweeted_status"]["entities"]["hashtags"],
                    'retweet_count': status._json["retweet_count"],
                }
            self.tweets.append(status_refined)
        return self.tweets

    def searchByKeywordPro(self, query, since="", until="", maxResults=None):
        """
        If user doesn't pass max no of tweets to fetch,
        it will fetch all available tweets, else fetches specific no of tweets
        """

        tweetsList = []
        if(not maxResults):
            tweetList, next_token = self.api.search_30_day(
                environment_name="developer", query=query, toDate=until, fromDate=since)
            tweetsList.append(tweetList)
            while(next_token):
                tweetList, next_token = self.api.search_30_day(
                    environment_name="developer", query=query, toDate=until, fromDate=since, next=next_token)
                tweetsList.append(tweetList)
        else:
            tweetList, next_token = self.api.search_30_day(
                environment_name="developer", query=query, toDate=until, fromDate=since)
            tweetsList.append(tweetList)
            maxResults -= len(tweetList)
            while(next_token and maxResults > 0):
                tweetList, next_token = self.api.search_30_day(
                    environment_name="developer", query=query, toDate=until, fromDate=since, next=next_token)
                tweetsList.append(tweetList)
                maxResults -= len(tweetList)
        for status in tweetsList:
            createdDate = parser.parse(str(status._json["created_at"]).strip())
            createdDate = createdDate.replace(
                tzinfo=pytz.utc) - createdDate.utcoffset()
            status_refined = {
                'keyword': query,
                '_id': status._json["id"],
                'created_at': createdDate,
                'tweetText': status._json["text"],
                'hashtags': status._json["entities"]["hashtags"],
                'userLoc': status._json["user"]["location"],
                'tweetGeo': status._json["geo"],
                'tweetCoordinates': status._json["coordinates"],
                'tweetPlace': status._json["place"],
                'retweet': {},
                'quote': {},
            }
            if hasattr(status, "quoted_status"):
                if "extended_tweet" in status._json["quoted_status"].keys():
                    print("Taking the expanded tweet")
                    status_refined['tweetText'] = status._json["quoted_status"]["extended_tweet"]["full_text"]
                else:
                    status_refined['tweetText'] = status._json["quoted_status"]["text"]
                status_refined['quote'] = {
                    'original_retweet_id': status._json["quoted_status"]["id"],
                    'origUserLoc': status._json["quoted_status"]["user"]["location"],
                    'origTweetLoc': status._json["quoted_status"]["geo"],
                    'origTweetPlace': status._json["quoted_status"]["place"],
                    'origTweetCoord': status._json["quoted_status"]["coordinates"],
                    'origHashtags': status._json["quoted_status"]["entities"]["hashtags"],
                    'retweet_count': status._json["quote_count"],
                }
            elif hasattr(status, "retweeted_status"):
                print(status._json["retweeted_status"])
                if "extended_tweet" in status._json["retweeted_status"].keys():
                    print("Taking the expanded tweet")
                    status_refined['tweetText'] = status._json["retweeted_status"]["extended_tweet"]["full_text"]
                else:
                    status_refined['tweetText'] = status._json["retweeted_status"]["text"]
                status_refined['retweet'] = {
                    'original_retweet_id': status._json["retweeted_status"]["id"],
                    'origUserLoc': status._json["retweeted_status"]["user"]["location"],
                    'origTweetLoc': status._json["retweeted_status"]["geo"],
                    'origTweetPlace': status._json["retweeted_status"]["place"],
                    'origTweetCoord': status._json["retweeted_status"]["coordinates"],
                    'origHashtags': status._json["retweeted_status"]["entities"]["hashtags"],
                    'retweet_count': status._json["retweet_count"],
                }
            elif hasattr(status, "extended_tweet"):
                if "extended_tweet" in status._json.keys():
                    status_refined['tweetText'] = status._json["extended_tweet"]["full_text"]
            self.tweets.append(status_refined)
        return self.tweets

    def printResults(self):
        """Print all the tweets"""
        for tweet in self.tweets:
            print(tweet)
            print("---------------------\n")



