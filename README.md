# Twitter Sentiment Analysis

### Objectives:
* Take a person's name, a county in Minneapolis, and a list of topics from a configuration file.
* Request tweets which reference the person's name and were initiated in the named county.
* Perform Data Processing/Cleaning.
* Perform Sentiment Analysis on processed information and store result in db.
* Time-series visualization of information.

### Future Work:
* Expand to other social media sites.



### Tech Stack:
* [Python 3](https://www.python.org/downloads/) - Used Language. Can use [Anaconda](https://www.anaconda.com/distribution/) for `Windows`
* Current Required Major Modules (Minor Modules via requirements.txt)
  * [Tweepy](https://anaconda.org/conda-forge/tweepy) - Python Module for Twitter API
  * [Praw](https://praw.readthedocs.io/en/v3.6.0/) - Python Module for Reddit API
  * [Pyyaml](https://pypi.org/project/PyYAML/) - Python Module to read YAML configs
  * [NLTK](https://www.nltk.org/) - Python Module for Natural Language Processing
  * [NeuralCoref](https://github.com/huggingface/neuralcoref) - Python Module to identify and resolve the coreference.
  * [Spacy 2.1.0 version](https://spacy.io/) - Industrial grade alternative to NLTK.
  * [FLASK-RESTFUL](https://pypi.org/project/Flask-RESTful/)
  * [PyMongo](https://pypi.org/project/pymongo/)
  * [MongoDB](https://www.mongodb.com/)
  * [Ktrain](https://github.com/amaiya/ktrain)
  * [Tensorflow v 1.15](https://www.tensorflow.org/)

### Running project
* `pip install -r requirements.txt`
* `python setup.py` : Admin permission
* `python runner.py`
  

### Configuration
*  **aspectConfigs.yml**: Configure aspects related things here; eg. (aspect keywords, cache timeout)
* **modelConfigs.yml**: Configure model related things for eg. (classifier selection, classifier registration)
* config files can be read using the **config readers** available in helpers.

### new folders
* **cache**: it caches the fetched related words used during aspect identification. Cache life span can be set in aspectConfigs.yml in cache_time_out field.
* **classify/models**: models folder holds the trained models in serialized form (pickle). Models folder can be changed in modelConfigs.yml

### new python files (only important ones)
* **classify/classifier.py**: classification based on the model seleted from modelConfigs.yml
* **processing/aspectsIdentifier.py**: identifies the aspects of the sentence based on the aspectConfigs.yml
