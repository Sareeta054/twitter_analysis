'''
    author: Bipin
'''

import requests
import urllib
import json

# Thinking on finding aspects
# we came up with the idea of finding similar words
# by comparing the word embeddings of the words in latent space
# we found that MIT has built ConceptNet; a knowledge graph based on word embeddings
# ConcpetNet also has a free API to access the knowledge graph which is very convinient

# relatedwords.org uses ConceptNet along with other algorithm inside
# to come up with the related words
# Upon experimenting with both sources; suggestions from
# relatedwords.org looks more appropriate for our use case 
def fetchRelatedWords(word):
    '''
    using https://relatedwords.org/ find the related words to the given word
    returns list of dict, in descending order of relatedness score
    for eg:
        {'word': 'health', 'score': 27.688784532941305, 'from': 'cn5,ol,wiki,swiki'}
        {'word': 'medicine', 'score': 24.990184188413064, 'from': 'cn5,ol,w2v,wiki,swiki'}
        {'word': 'treatment', 'score': 8.791995623154092, 'from': 'cn5,cn5,w2v,swiki'}
        ...
    '''

    # properly quote url (eg: health care -> health%20care)
    url = "https://relatedwords.org/api/related?term=" + urllib.parse.quote(word)
    try:
        page = requests.get(url)
        return json.loads(page.content)
    except Exception as e:
        print("-"*40, "ERROR:\n", e, "\n", "-"*40)
        return []




# print(fetchRelatedWords("health care"))