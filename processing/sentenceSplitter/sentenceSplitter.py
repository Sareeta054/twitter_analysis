'''
    author: Bipin Oli
'''

import os, sys, re
import nltk



if __name__ == "__main__":
    project_root_path = os.path.split(os.path.dirname(os.path.realpath(__file__)))[0]
    project_root_path = os.path.split(project_root_path)[0]
    sys.path.insert(0, project_root_path)
    
    

from processing.sentenceSplitter.conjunctionSentenceSplitter import SplitWithConjuction
from processing.sentenceSplitter.sentenceSimplifier import Simplifier
from processing.spacySingleton import SpacyProvider





# splitting rules
# 1. replacing reference words like he, it, .. by suitable noun from sentence (resolving coreference)
# 2. splitting sentence (full stops)
# 3. splitting sentence with (but, because, ...)
# 4. splitting sentence with (either or, neither nor)
# 4. splitting sentence with (and, ',') into multiple sentences


class SentenceSplitter:

    def __init__(self):
        self.nlp = SpacyProvider.getInstance()

    def _sentenceSplitter(self, sentence):
        sentence = u"{}".format(sentence)
        doc = self.nlp(sentence)
        retval = []
        for sent in doc.sents:   
            retval.append(sent.text)
        return retval
    
    def _butGroupSplitter(self, sentence):
        but_group = ['but', 'because', 'though', 'however', 'although', 'merely', 'yet', 'nevertheless', 'nonetheless', 'except', 'therefore', 'anyway', 'perhaps', 'whereas', 'furthermore', 'besides', 'moreover', 'otherwise', 'furthermore', ]
        regex = r"\s+(?:" + "|".join(but_group) + r")\s+"
        return re.split(regex, sentence)



    def _eitherOrGroupSplitter(self, sentence):
        # TODO: may be its needed but lets igore this for now
        return [sentence]



    def _conjunctionSplitter(self, sentence):
        conjSplitter = SplitWithConjuction()
        return conjSplitter.split(sentence)



    def _flatList(self, lst):
        '''
            flattens the nested listed (list of lists) into a single list of elements
        '''
        retval = []
        for i in lst: 
            if type(i) == list: 
                retList = self._flatList(i)
                for r in retList:
                    retval.append(r)
            else: 
                retval.append(i)
        return retval



    def _unbreakApostrophe(self, sentence):
        '''
        Input: They 're working hard.
        Output: They're working hard.

        Input: I do n't want this.
        Output: I don't want this.
        '''
        retval = ""
        for s in str(sentence).split():
            if not re.search(r'\'|’', s):
                retval += " "
            retval += s
        return retval

    def _listOperation(self, lst, operation):
        '''
            perform the given operation function for every list item
        '''
        nextLst = []
        for l in lst:
            nextLst.append(operation(l))
        return list(set(self._flatList(nextLst)))



    def splitSentenceVerbose(self, sentence):
        '''
            Split sentence by the pipeline different kinds of splitters
            And provides debug information in every step
                splitting pipeline:
                    1. replacing reference words like he, it, .. by suitable noun from sentence (resolving coreference)
                    2. splitting sentence (full stops)
                    3. splitting sentence with (but, because, ...)
                    4. splitting sentence with (either or, neither nor)
                    4. splitting sentence with (and, ',') into multiple sentences
        # '''
        # print("before: ", sentence)
        lst = self._sentenceSplitter(sentence)
        # print("\nafter sentence splitting: ", lst)

        simplifier = Simplifier()
        lst = simplifier.getSplitSentences(lst)
        print("\nafter simplifier: ", lst)
        
        lst = self._listOperation(lst, self._butGroupSplitter)
        print("\nafter butGroup splitting: ", lst)

        lst = self._listOperation(lst, self._eitherOrGroupSplitter)
        print("\nafter eitherorGroup splitting: ", lst)
        
        lst = self._listOperation(lst, self._conjunctionSplitter)
        print("\nafter conjunction splitting: ", lst)
        
        lst = self._listOperation(lst, self._unbreakApostrophe)
        print("\nafter unbreaking apostrophe: ", lst)

        print(lst)
        
        return lst
        
        


    def splitSentence(self, sentence):
        '''
            Split sentence by the pipeline different kinds of splitters
                splitting pipeline:
                    1. replacing reference words like he, it, .. by suitable noun from sentence (resolving coreference)
                    2. splitting sentence (full stops)
                    3. splitting sentence with (but, because, ...)
                    4. splitting sentence with (either or, neither nor)
                    4. splitting sentence with (and, ',') into multiple sentences
        '''
        lst = self._sentenceSplitter(sentence)
        
        simplifier = Simplifier()
        lst = simplifier.getSplitSentences(lst)
        
        lst = self._listOperation(lst, self._butGroupSplitter)
        lst = self._listOperation(lst, self._eitherOrGroupSplitter)
        lst = self._listOperation(lst, self._conjunctionSplitter)
        lst = self._listOperation(lst, self._unbreakApostrophe)
        return lst





if __name__ == "__main__":
    test0 = "Ram called his friend Hari."
    test1 = "The pricing, service and location is just perfect but its too bad we cannot depends on its availability."
    test2 = "Health care and scooling are free in Canada."
    test3 = "Getting a job is a blast here in XYZ due to economic boom however the transportation is just terrible here."
    test4 = "Despite huge criticisms, I must say; his performance in ABC was admirable."
    test5 = "Plot was good, acting was bad."
    test6 = "plot good acting bad"
    test7 = "plot was good but acting was bad"
    test8 = "bad acting but a good movie"
    test9 = "mix of both good and bad"
    test10 = "good movie with bad acting"
    test11 = "good location and plot but bad acting and cinematography"
    test12 = "good on issues like immigration and healthcare but I didn't like her agenda on climate change and economy"
    test13 = "issues like immigration and healthcare are represented properly but her agenda on climate change and economic development doesn't look promising"
    test14 = "Overall amazing phone with killer display and processor with only downside benig its 3000mAh battery"
    test15 = "If i had her number i would have definitely called her"
    test16 = "Lion and tiger are chasing a deer and fox is chasing a rabbit"
    test17 = "My father, who is a President, is an honest man."
    test18 = "My brother and sister, who are the members of the association are working hard."

    tests = [test0, test1, test2, test3, test4, test5, test6, test7, test8, test9, test10, test11, test12, test13, test14, test15, test16]
    small_tests = [test0, test1, test2, test3, test16]
    curated_tests = [test0, test1, test7, test11, test17, test18]

    splitter = SentenceSplitter()

    for test in curated_tests:
        print("\n\n splitting : ", test)
        print(splitter.splitSentence(test))
        print("-"*100)

    while True:
        print("input: ", end="")
        sent = input()
        print("\n")
        print(splitter.splitSentenceVerbose(sent))
        print("-"*100)
