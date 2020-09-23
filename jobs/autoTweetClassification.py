import sys, os

if __name__ == "__main__":
    project_root_path = os.path.split(
        os.path.dirname(os.path.realpath(__file__)))[0]
    sys.path.insert(0, project_root_path)
from functools import reduce
from extraction.twitterHandle import TwitterHandle
from processing.preprocess import Preprocessor
import datetime
from helpers.dbHelper import MongodbInteracter
from classify.classifier import Classifier

class AutoTweetClassifcation:

    def __init__(self):
        self.classifier = Classifier()

    def __processTweets(self, daily_tweets, existing_tweets):
        existing_tweets_ids = [x['id'] for x in existing_tweets]
        required_location = []
        required_location = list(map(lambda x: str(x).lower(), required_location))
        def filter_loc(x):
            flag = False
            if required_location:
                if x['retweet'] and x['retweet']['origTweetPlace'] and x['retweet']['origTweetPlace']['full_name']:
                    flag = flag or x['retweet']
                if x['retweet'] and x['retweet']['origUserLoc']:
                    flag = flag or reduce(lambda a,b: a or b, [str(x['retweet']['origUserLoc'].lower()).__contains__(reqLoc) for reqLoc in required_location])
                if x['tweetPlace'] and x['tweetPlace']['full_name']:
                    flag = flag or reduce(lambda a,b : a or b,[str(x['tweetPlace']['full_name'].lower()).__contains__(reqLoc) for reqLoc in required_location])
                flag = flag or reduce(lambda a,b: a or b, [str(x['userLocation'].lower()).__contains__(reqLoc) for reqLoc in required_location])
            else:
                flag = True
            return flag
        processedTweets = list(filter(filter_loc, daily_tweets))
        if existing_tweets_ids and existing_tweets:
            for x in processedTweets:
                def map_func(z):
                    if z['id'] == x['retweet']['original_retweet_id']:
                        z['count'] += 1
                    return z
                if x['retweet']:
                    existing_tweets = list(map(map_func, existing_tweets))
            processedTweets = list(filter(lambda x: False if x['retweet'] and x['retweet']['original_retweet_id'] in existing_tweets_ids or x['_id'] in existing_tweets_ids else True , processedTweets))
        print("\nProcessedTweets\n", processedTweets)
        return processedTweets

    def __classifyTweets(self, tweets):
        result = [{'_id': x['_id'], 'classification' : self.classifier.classify(x['tweetText']), 'count' : 1} for x in tweets]
        return result
    
    def run(self):
        datetoday = datetime.date.today()
        dateoffset = datetime.timedelta(days=1)
        weekoffset = datetime.timedelta(days=7)
        db = MongodbInteracter(dbName='tsa', collectionName='twitter')
        query = {'created_at' : {'$gte' : datetime.datetime.combine(datetoday - weekoffset, datetime.time()), '$lt': datetime.datetime.combine(datetoday + dateoffset, datetime.time())}}
        daily_tweets = db.fetchContents(query=query)
        db = MongodbInteracter(dbName='tsa', collectionName='twitter_result')
        existing_tweets = db.fetchContents()
        processedTweets = self.__processTweets(daily_tweets=daily_tweets, existing_tweets=existing_tweets)
        result = self.__classifyTweets(processedTweets)
        db.postContents(result)
        

if __name__ == '__main__':
    fetch = AutoTweetClassifcation()
    fetch.run()
