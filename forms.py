from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DateField, SelectMultipleField, BooleanField, FormField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Length

class StudentGoalForm(FlaskForm):
    title = StringField('Short goal title:', validators=[
                        DataRequired(), Length(max=140)])
    description = StringField('Goal description:', validators=[
                              DataRequired(), Length(max=250)])
    submit = SubmitField('Save student goal')
