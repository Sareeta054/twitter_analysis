'''
    author: Bipin Oli
'''

import pickle 
import os, sys, json, datetime



if __name__ == "__main__":
    project_root_path = os.path.split(os.path.dirname(os.path.realpath(__file__)))[0]
    sys.path.insert(0, project_root_path)



from helpers.aspectConfigReader  import AspectConfigReader
from helpers.relatedWordsFetcher import fetchRelatedWords
from helpers.wordsComparator import lemmatize



class AspectIdentifier:

    def __init__(self):
        cache_fn = AspectConfigReader.getCachePath()
        self.cache_folder = os.path.join(os.path.split(os.path.dirname(os.path.realpath(__file__)))[0], 'cache')
        self.cache_path = os.path.join(self.cache_folder, cache_fn)
        self.aspects = AspectConfigReader.getAspects()
        self.relatedWordsLemmatized = self._retriveLemmatizedRelatedWords()

        

    def identify(self, sentence):
        '''
        Identify the aspects of the sentence.
        Returns the list of the identified aspects.
        '''
        words = sentence.split(" ")
        retAspects = set()

        for word in words:
            for aspect in self.aspects:
                for relatedWord in self.relatedWordsLemmatized[aspect]:
                    if (str(lemmatize(word)).lower()).__contains__(str(relatedWord).lower()):
                        retAspects.add(aspect)
        return list(retAspects)




    def _lemmatizeRelatedWords(self):
        if AspectConfigReader.isStatic():
            relatedWords = self._retrieveRelatedWordsStaticJson()
        else:
            relatedWords = self._getRelatedWords()

        if not AspectConfigReader.isStatic():
            # if any aspect is not in relatedWords
            # that means config file has been updated 
            # so cache much be updated as well
            for aspect in self.aspects:
                if aspect not in relatedWords:
                    self._cacheRelatedWords()
                    break

        relatedWordsLemmatized = {}
        
        for aspect in relatedWords:
            for word in relatedWords[aspect]:
                if aspect not in relatedWordsLemmatized:
                    relatedWordsLemmatized[aspect] = []
                relatedWordsLemmatized[aspect].append(lemmatize(word))

        # remove duplicate lemmas
        for aspect in relatedWordsLemmatized:
            relatedWordsLemmatized[aspect] = list(set(relatedWordsLemmatized[aspect]))        
        return relatedWordsLemmatized
        



    def _saveLemmatizedRelatedWords(self, _lemmatizeRelatedWords):
        json_path = os.path.join(self.cache_folder, "lemmatized_" + AspectConfigReader.getJsonPath())
        with open(json_path, 'w') as outfile:
            if 'cache_time_out' in _lemmatizeRelatedWords:
                _lemmatizeRelatedWords.pop('cache_time_out')
            json.dump(_lemmatizeRelatedWords, outfile)




    def _retriveLemmatizedRelatedWords(self):
        json_path = os.path.join(self.cache_folder, "lemmatized_" + AspectConfigReader.getJsonPath())
        if not os.path.exists(json_path) or self._needToRefreshCache():
            lemmaRelWds = self._lemmatizeRelatedWords()
            self._saveLemmatizedRelatedWords(lemmaRelWds)
            return lemmaRelWds
        with open(json_path) as json_file:
            data = json.load(json_file)
            return data




    def _needToRefreshCache(self):
        if not AspectConfigReader.isStatic():
            relatedWords = self._retrieveRelatedWordsFromCache()
            if (datetime.datetime.now() >= relatedWords["cache_time_out"]):
                return True
        return False




    def _getRelatedWords(self, verbose=False):
        '''
        return related words of aspects.
        It returns the info from cache if cache hasn't expired.
        '''
        if self._needToRefreshCache():
            if verbose:
                print("\n---- INFO: Cache is no longer valid. Hitting API for data ------ \n")
            self._cacheRelatedWords()
        if verbose:
            print("\n---- INFO: Cache is VALID. Returning data from cache ----- \n")
        return self._retrieveRelatedWordsFromCache()
        
        
        
        
        
    def _retrieveRelatedWordsStaticJson(self):
        json_path = os.path.join(self.cache_folder, AspectConfigReader.getJsonPath())
        if not os.path.exists(json_path):
            self._saveRelatedWordsJson()
        with open(json_path) as json_file:
            data = json.load(json_file)
            return data





    def _saveRelatedWordsJson(self):
        relatedWords = self._getRelatedWords()
        json_path = os.path.join(self.cache_folder, AspectConfigReader.getJsonPath())
        with open(json_path, 'w') as outfile:
            relatedWords.pop('cache_time_out')
            json.dump(relatedWords, outfile)





    def _fetchRelatedWords(self):
        relatedWords = {}
        for aspect in self.aspects:
            words = fetchRelatedWords(aspect)
            if (len(words) < 1):
                print("\n---- ERROR ---: couldn't fetch related words of " + aspect + "\n")
                continue
            toAdd = []
            for data in words:
                toAdd.append(data['word'])
            relatedWords[aspect] = toAdd
        return relatedWords




    def _cacheRelatedWords(self):
        relatedWords = self._fetchRelatedWords()
        cache_delta = AspectConfigReader.getCacheTimeout()
        relatedWords["cache_time_out"] = datetime.datetime.now() + datetime.timedelta(hours=cache_delta)
        pickle.dump(relatedWords, open(self.cache_path, "wb"))





    def _retrieveRelatedWordsFromCache(self):
        if not os.path.exists(self.cache_path):
            self._cacheRelatedWords()
        relatedWords = pickle.load(open(self.cache_path, "rb"))
        return relatedWords








# ---------------------------- Testing -------------------------------

if __name__ == "__main__":
    ai = AspectIdentifier()
    print("Input please:", end="")
    x = input()
    print("\n"*1)
    print("Aspects:",  end="")
    print(ai.identify(x))
    # print(ai.identify("I want to graduate this summer."))
    # print(ai.identify("Chinese government is trying to undermine Honkong."))
    # print(ai.identify("I was fired."))
    # print(ai.identify("New immigrants have difficulty getting jobs."))