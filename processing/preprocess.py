# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 16:51:41 2019

@author: alok.regmi
"""
import re
import emoji
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import operator

from processing.coreferenceResolver import resolveCoreference


class Preprocessor:
    
    def clean(self, tweet):
        tweet = tweet.lower()
        tweet = self._clearTwitterSymbols(tweet)
        tweet = self._clearPunctuation(tweet)
        tweet = self._demojize(tweet)
        return tweet

    
    def _resolveCoreference(self,tweet):
        return resolveCoreference(tweet);
        

    def _clearTwitterSymbols(self,tweet):
       
        # can add logic to handle the hashtag matchs into words here if we want


        # convert string to lowercase 
        tweet = tweet.lower()
        # remove retweets and their original_users and use keyword RETWEET
        tweet = re.sub(r'^rt', " RETWEET ", tweet)
        # remove user_mentions and use keyword USER_MENTION
        tweet = re.sub(r'@\w{1,15}[.]*', " USER_MENTION ", tweet)
        # replace hashtags with keyword HASHTAG
        tweet = re.sub(r'#(\w)*[.]*', " HASHTAG ", tweet)
        # remove url links and use keyword URL
        tweet = re.sub(r'(https://)[\S]*'," URL ", tweet)
        
        # punctuation removal
        # replace dots and ellipses(...) with space 
        tweet = re.sub(r'\.{2,}', ' ', tweet)
        
        # remove punctuation marks but protect exclamation marks
        regex = r"(?:^\'|^\"|\'$|\"$|\'\s*\'|\'\s*\'|\'\s*\"|\"\s*\'|\"\s*\"|\s+\"|\s+\'|\'\s+|\"\s+)"
        tweet = re.sub(regex, ' ', tweet)
        
        # convert all whitespaces into a single space
        tweet = re.sub(r'[\s]+', ' ', tweet)
        return tweet

        
    def _demojize(self,tweet):
        # replace emojis in unicode with their respective emotions
        emoji_sad = ([ '🤔','🤨','😐','😑','😶','🙄','😏','😣','🤐','😪','😴','😖',
        '😤','😦','🤯','😰','🥵','🥶','😳','🤪','😡','🤬','😷','🤒','🤕','🤢','🤮',
        '🤧','😈','👹','👺','💩','😾'])
        retval = ""
        for i in tweet:
            if i in emoji.UNICODE_EMOJI:
                analyser = SentimentIntensityAnalyzer()
                score = analyser.polarity_scores(i)
                if max(score.items(), key=operator.itemgetter(1))[0] is 'neu':
                    if i in emoji_sad:
                        retval += " emo_neg"
                    else:
                        retval += " emo_pos"
                elif max(score.items(), key=operator.itemgetter(1))[0] is 'pos' or 'compound':
                    retval += ' emo_pos'
                else:
                    retval += ' emo_neg'
            else:
                retval += i
        return retval


    def _removeTwitterSymbols(self, tweet):
        """ This function is intended to clean tweets further for passing
        for sentiment classification task 
        """
        
        # remove retweets and their original_users and use keyword RETWEET
        tweet = re.sub(r'RETWEET', " ", tweet)
        # remove user_mentions and use keyword USER_MENTION
        tweet = re.sub(r'USER_MENTION', " ", tweet)
        # replace hashtags with keyword HASHTAG
        tweet = re.sub(r'HASHTAG ', " ", tweet)
        # remove url links and use keyword URL
        tweet = re.sub(r'URL'," ", tweet)
        
        # convert string to lowercase 
        tweet = tweet.lower()
        # punctuation removal
        # replace dots and ellipses(...) with space 
        tweet = re.sub(r'\.{2,}', ' ', tweet)
        
        # remove punctuation marks but protect exclamation marks
        regex = r"(?:^\'|^\"|\'$|\"$|\'\s*\'|\'\s*\'|\'\s*\"|\"\s*\'|\"\s*\"|\s+\"|\s+\'|\'\s+|\"\s+)"
        tweet = re.sub(regex, ' ', tweet)
        
        # convert all whitespaces into a single space
        tweet = re.sub(r'[\s]+', ' ', tweet)

        return tweet


    # To do: Change hashtags to individual words that can be added to the sentence tokens later
    def _hashtagToWords(self,hashtag):
        return None


    def _clearPunctuation(self,tweet):
        # remove brackets
        brackets = ['\(', '\{', '\[', '\)', '\}', '\]']
        regex = r'\s*(?:' + r'|'.join(brackets) + r')\s*'
        tweet = re.sub(regex, ' ', tweet)
        return tweet


    