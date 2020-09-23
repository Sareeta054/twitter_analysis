'''
    author: Bipin Oli
'''

import spacy 
import neuralcoref



class SpacyProvider:

    __spacy = None

    @staticmethod
    def getInstance():
        if SpacyProvider.__spacy == None:
            print(" --- creating spacy instance --- ")
            SpacyProvider.__spacy = spacy.load('en_core_web_sm')
            # neuralcoref.add_to_pipe(SpacyProvider.__spacy)
        return SpacyProvider.__spacy



if __name__ == "__main__":
    print(SpacyProvider.getInstance())