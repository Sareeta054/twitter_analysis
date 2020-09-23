# About

* This is the nodejs code that generates the sentences containing the keyword specified.
* Sentences containing aspects or related words can be generated and used to train the
BERT model similar to the way they did in **https://arxiv.org/abs/1903.09588** paper

## Steps
1.   read aspect config file
2.   fetch the related words
3.   generate sentences containing the aspect 
4.   generate sentences containing related words of aspect
5.   save sentences into json file along with their aspect
6.   the json file will be read by the classifier to classify the sentences
7.   classified sentences along with aspect will be used to train the BERT model