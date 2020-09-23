from flask_restful import Resource, request
from flask import jsonify
import json
from helpers.modelInitializer import ModelInitializer

class ModelResource(Resource):

    def post(self):
        data = request.json
        if not data or not self._checkPayloadValidity(data):
            return "Invalid Request", 400
        result = self._feedModel(data)
        return result, 200

    def get(self):
        return True, 200

    def _checkPayloadValidity(self, payload):
        return (False if list(filter(lambda x: not (x == 'payload'), payload.keys())) else True) and ('payload' in payload.keys())

    def _feedModel(self, data):
        classifier = ModelInitializer._getClassifier()
        result = classifier.classify(data['payload'])
        return result