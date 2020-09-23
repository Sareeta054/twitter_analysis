import sys, os

if __name__ == "__main__":
    project_root_path = os.path.split(
        os.path.dirname(os.path.realpath(__file__)))[0]
    sys.path.insert(0, project_root_path)
from extraction.twitterHandle import TwitterHandle
from helpers.dbHelper import MongodbInteracter
import datetime

class AutoTweetExtraction:

    def __init__(self):
        self.db = MongodbInteracter(dbName='tsa', collectionName='twitter')
        self.twitterHandle = TwitterHandle()

    def run(self):
        datetoday = datetime.date.today()
        dayoffset = datetime.timedelta(days=1)
        previousday = datetoday - dayoffset
        amy_tweets = self.twitterHandle.searchByKeyword(
            "amy klobuchar", since=previousday)
        self.db.postContents(amy_tweets)

if __name__ == "__main__":
    ext = AutoTweetExtraction()
    ext.run()