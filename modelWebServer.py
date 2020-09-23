"""
@author: Aashish
"""
import os
import sys
if __name__ == "__main__":
    project_root_path = os.path.split(os.path.dirname(os.path.realpath(__file__)))[0]
    sys.path.insert(0, project_root_path)
from flask import Flask
from flask_restful import Api
from webResources.modelResource import ModelResource

if __name__ == "__main__":
    app = Flask(__name__, template_folder='webFeatures')
    api = Api(app)
    api.add_resource(ModelResource, "/testModel", endpoint="model")
    app.run(host='0.0.0.0', port=5050)
