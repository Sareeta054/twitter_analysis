from flask_restful import Resource, request
from flask import render_template, make_response
from webFeatures.form import PipeLineForm
from processing.preprocess import Preprocessor
from classify.classifier import Classifier
class FormResource(Resource):
    def get(self):
        return self._handle()

    def post(self):
        return self._handle()

    def _handle(self):
        form = PipeLineForm()
        headers = {'Content-Type': 'text/html'}
        result_header = {'Content-Type': 'application/json'}
        if form.validate_on_submit():
            classifier = Classifier()
            pruner = Preprocessor()
            cleaned_input = pruner.clean(form.text.data)
            return make_response(classifier.classify(cleaned_input), 200, result_header)
        return make_response(render_template('demoForm.html', form=form), 200, headers)
