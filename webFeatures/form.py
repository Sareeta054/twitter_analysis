from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired

class PipeLineForm(FlaskForm):
    text = TextAreaField('Sample Text Input', validators=[DataRequired()])
    submit = SubmitField('Submit')