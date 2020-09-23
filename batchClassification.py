'''
    author: Bipin Oli
'''

from helpers.dbHelper import MongodbInteracter
from classify.classifier import Classifier
from processing.preprocess import Preprocessor

class BatchClassification:

    def __init__(self):
        print("batch")
        self.classifier = Classifier()
        self.preprocessor = Preprocessor()

    def run(self, options):
        pass

    def runAll(self):
        '''
        Classify all tweets and store the classification in database
        '''
        dbInteractor = MongodbInteracter("tsa", "twitter")
        tweets = dbInteractor.fetchContents()
        for tweet in tweets:
            print("processing tweet: ", tweet['_id'])
            text = tweet['tweetText']
            text = self.preprocessor.clean(text)
            result = self.classifier.classify(text, verbose=False) 
            tweet['classification'] = result
            dbInteractor.replaceOnce(tweet)
        print("---- Batch run Complete ----")


if __name__ == "__main__":
    batch = BatchClassification()
    batch.runAll()