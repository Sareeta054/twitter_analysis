'''
    author: Bipin Oli
'''

'''
    This is the complete code for training a NaiveBayes Classifier
'''


from nltk.corpus import twitter_samples
from nltk.tokenize import TweetTokenizer


def log(msg):
    print("\n\n", "-"*30, " ", msg, " ", "-"*30)



# file ids
log("file ids")
print(twitter_samples.fileids())


pos_tweets = twitter_samples.strings('positive_tweets.json')
neg_tweets = twitter_samples.strings("negative_tweets.json")
pos_neg_tweets = twitter_samples.strings("tweets.20150430-223406.json")

# dataset size
log("size of dataset")
print("positive: ", len(pos_tweets))
print("negative: ", len(neg_tweets))
print("another(pos+neg): ", len(pos_neg_tweets))

# tokenizing tweets
twwet_tokenizer = TweetTokenizer(preserve_case=False, strip_handles=True, reduce_len=True)

log("Tokenizing Tweets")
print("before: ", pos_tweets[0])
print("after: ", twwet_tokenizer.tokenize(pos_tweets[0]))

# ---------------------------------------------------------------------------------------------------------------------
# cleaning tweets
'''
– Remove stock market tickers like $GE
– Remove retweet text “RT”
– Remove hyperlinks
– Remove hashtags (only the hashtag # and not the word)
– Remove stop words like a, and, the, is, are, etc.
– Remove emoticons like :), :D, :(, :-), etc.
– Remove punctuation like full-stop, comma, exclamation sign, etc.
– Convert words to Stem/Base words using Porter Stemming Algorithm. E.g. words like ‘working’, ‘works’, and ‘worked’ will be converted to their base/stem word “work”.
'''
log("Cleaning Tweets")

import string
import re
 
from nltk.corpus import stopwords 
stopwords_english = stopwords.words('english')
 
from nltk.stem import PorterStemmer
stemmer = PorterStemmer()
 
from nltk.tokenize import TweetTokenizer
 
# Happy Emoticons
emoticons_happy = set([
    ':-)', ':)', ';)', ':o)', ':]', ':3', ':c)', ':>', '=]', '8)', '=)', ':}',
    ':^)', ':-D', ':D', '8-D', '8D', 'x-D', 'xD', 'X-D', 'XD', '=-D', '=D',
    '=-3', '=3', ':-))', ":'-)", ":')", ':*', ':^*', '>:P', ':-P', ':P', 'X-P',
    'x-p', 'xp', 'XP', ':-p', ':p', '=p', ':-b', ':b', '>:)', '>;)', '>:-)',
    '<3'
    ])
 
# Sad Emoticons
emoticons_sad = set([
    ':L', ':-/', '>:/', ':S', '>:[', ':@', ':-(', ':[', ':-||', '=L', ':<',
    ':-[', ':-<', '=\\', '=/', '>:(', ':(', '>.<', ":'-(", ":'(", ':\\', ':-c',
    ':c', ':{', '>:\\', ';('
    ])
 
# all emoticons (happy + sad)
emoticons = emoticons_happy.union(emoticons_sad)
 
def clean_tweet(tweet):
    # remove stock market tickers like $GE
    tweet = re.sub(r'\$\w*', '', tweet)
 
    # remove old style retweet text "RT"
    tweet = re.sub(r'^RT[\s]+', '', tweet)
 
    # remove hyperlinks
    tweet = re.sub(r'https?:[\S]+', '', tweet)
    
    # remove hashtags
    # only removing the hash # sign from the word
    tweet = re.sub(r'#', '', tweet)
 
    # tokenize tweets
    tokenizer = TweetTokenizer(preserve_case=False, strip_handles=True, reduce_len=True)
    tweet_tokens = tokenizer.tokenize(tweet)
 
    tweet_clean = []    
    for word in tweet_tokens:
        if (word not in stopwords_english and # remove stopwords
              word not in emoticons and # remove emoticons
                word not in string.punctuation): # remove punctuation
            #tweets_clean.append(word)
            stem_word = stemmer.stem(word) # stemming word
            tweet_clean.append(stem_word)
 
    return tweet_clean

# ---------------------------------------------------------------------------------------------------------------------


# Feature Extraction

# feature extractor function
def bag_of_words(tweet):
    words = clean_tweet(tweet)
    words_dictionary = dict([word, True] for word in words)    
    return words_dictionary

# positive tweets feature set
pos_tweets_set = []
for tweet in pos_tweets:
    pos_tweets_set.append((bag_of_words(tweet), 'pos'))    
 
# negative tweets feature set
neg_tweets_set = []
for tweet in neg_tweets:
    neg_tweets_set.append((bag_of_words(tweet), 'neg'))

log("Positive Tweets, Negative tweets")
print(len(pos_tweets_set), len(neg_tweets_set))


# 80 - 20 train test split
# 1000/5000 data for testing

# radomize pos_reviews_set and neg_reviews_set
# doing so will output different accuracy result everytime we run the program
from random import shuffle 
shuffle(pos_tweets_set)
shuffle(neg_tweets_set)
 
test_set = pos_tweets_set[:1000] + neg_tweets_set[:1000]
train_set = pos_tweets_set[1000:] + neg_tweets_set[1000:]
 
print(len(test_set),  len(train_set)) # Output: (2000, 8000)

# ---------------------------------------------------------------------------------------------------------------------


# Training using Naive Bayes Classifier

from nltk import classify 
from nltk import NaiveBayesClassifier

classifier = NaiveBayesClassifier.train(train_set)

accuracy = classify.accuracy(classifier, test_set)
log("Testing accuracy")
print(accuracy)

log("20 most important features")
print(classifier.show_most_informative_features(20))

# --------------------------------------------------------
# save the trained model

import pickle 
pickle.dump(classifier, open("naiveBayesModel.pkl", "wb"))



# ---------------------------------------------------------------------------------------------------------------------

# Testing

log("Testing")

print("Type in tweet for classification: ", end=" ")
custom_tweet = input()

custom_tweet_set = bag_of_words(custom_tweet)

print(custom_tweet_set)

print("Prediction: ", classifier.classify(custom_tweet_set))

# probability result
prob_result = classifier.prob_classify(custom_tweet_set)
print ("probability distribution: ", prob_result)
print ("prediction: ", prob_result.max()) 
print ("P(neg): ", prob_result.prob("neg"))
print ("P(pos): ", prob_result.prob("pos"))


# ---------------------------------------------------------------------------------------------------------------------
# Test Metrics


from collections import defaultdict
 
actual_set = defaultdict(set)
predicted_set = defaultdict(set)
 
actual_set_cm = []
predicted_set_cm = []
 
for index, (feature, actual_label) in enumerate(test_set):
    actual_set[actual_label].add(index)
    actual_set_cm.append(actual_label)
 
    predicted_label = classifier.classify(feature)
 
    predicted_set[predicted_label].add(index)
    predicted_set_cm.append(predicted_label)
    

log("Test Metrics")
'''
    Accuracy = (TP + TN) / (TP + TN + FP + FN)
    Precision = (TP) / (TP + FP)
    Recall = (TP) / (TP + FN)
    F1 Score = 2 * (precision * recall) / (precision + recall)
'''

from nltk.metrics import precision, recall, f_measure, ConfusionMatrix
 
print('pos precision:', precision(actual_set['pos'], predicted_set['pos'])) 
print('pos recall:', recall(actual_set['pos'], predicted_set['pos'])) 
print('pos F-measure:', f_measure(actual_set['pos'], predicted_set['pos']))
 
print('neg precision:', precision(actual_set['neg'], predicted_set['neg']))
print('neg recall:', recall(actual_set['neg'], predicted_set['neg']))
print('neg F-measure:', f_measure(actual_set['neg'], predicted_set['neg']))


# confusion matrix
'''
           |   Predicted NO      |   Predicted YES     |
-----------+---------------------+---------------------+
Actual NO  | True Negative (TN)  | False Positive (FP) |
Actual YES | False Negative (FN) | True Positive (TP)  |
-----------+---------------------+---------------------+
'''

cm = ConfusionMatrix(actual_set_cm, predicted_set_cm)
print(cm.pretty_format(sort_by_count=True, show_percents=True, truncate=9))



# ---------------------------------------------------------------------------------------------------------------
# OUTPUT

'''

 ------------------------------   file ids   ------------------------------    
['negative_tweets.json', 'positive_tweets.json', 'tweets.20150430-223406.json']


 ------------------------------   size of dataset   ------------------------------
positive:  5000
negative:  5000
another(pos+neg):  20000


 ------------------------------   Tokenizing Tweets   ------------------------------
before:  #FollowFriday @France_Inte @PKuchly57 @Milipol_Paris for being top engaged members in my community this week :)
after:  ['#followfriday', 'for', 'being', 'top', 'engaged', 'members', 'in', 'my', 'community', 'this', 'week', ':)']   


 ------------------------------   Cleaning Tweets   ------------------------------


 ------------------------------   Positive Tweets, Negative tweets   ------------------------------
5000 5000
2000 8000


 ------------------------------   Testing accuracy   ------------------------------
0.7525


 ------------------------------   20 most important features   ------------------------------
Most Informative Features
                     sad = True              neg : pos    =     22.6 : 1.0
                      aw = True              neg : pos    =     21.7 : 1.0
                   arriv = True              pos : neg    =     19.8 : 1.0
                     x15 = True              neg : pos    =     19.0 : 1.0
                   cream = True              neg : pos    =     19.0 : 1.0
                  commun = True              pos : neg    =     16.3 : 1.0
                    lost = True              neg : pos    =     15.7 : 1.0
                   didnt = True              neg : pos    =     14.3 : 1.0
                     ugh = True              neg : pos    =     13.7 : 1.0
                       �😭 = True              neg : pos    =     13.0 : 1.0
                    poor = True              neg : pos    =     12.6 : 1.0
                unfortun = True              neg : pos    =     12.3 : 1.0
                     ice = True              neg : pos    =     12.2 : 1.0
               goodnight = True              pos : neg    =     11.7 : 1.0
                   invit = True              pos : neg    =     11.0 : 1.0
                influenc = True              pos : neg    =     11.0 : 1.0
                    tire = True              neg : pos    =     10.7 : 1.0
                  hungri = True              neg : pos    =     10.3 : 1.0
                   shame = True              neg : pos    =     10.3 : 1.0
                     via = True              pos : neg    =     10.2 : 1.0
None


 ------------------------------   Testing   ------------------------------
Type in tweet for classification:  I hate to wait for the bus. It drives me crazy @Rupesh @Bijay #crazyLife #sad
Prediction:  neg
probability distribution:  <ProbDist with 2 samples>
prediction:  neg
P(neg):  0.9969485155969436
P(pos):  0.003051484403056413


 ------------------------------   Test Metrics   ------------------------------
pos precision: 0.7482792527040315
pos recall: 0.761
pos F-measure: 0.7545860188398612
neg precision: 0.7568667344862665
neg recall: 0.744
neg F-measure: 0.7503782148260213
    |      n      p |
    |      e      o |
    |      g      s |
----+---------------+
neg | <37.2%> 12.8% |
pos |  11.9% <38.0%>|
----+---------------+
(row = reference; col = test)

'''