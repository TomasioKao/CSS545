from unicodedata import category
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, BooleanField, SelectField, TextAreaField
from wtforms.validators import DataRequired, NumberRange
from wtforms.widgets.html5 import NumberInput

position_options = [
    ('forwards', 'forwards'),
    ('centers', 'centers'),
    ('guards', 'guards')
]

class CreateTalentForm(FlaskForm):
    number = IntegerField('number', validators=[DataRequired()])
    name = StringField('name', validators=[DataRequired()])
    img = StringField('img', validators=[DataRequired()])
    position = SelectField('position', choices = position_options)
    country = StringField('country', validators=[DataRequired()])
    height = IntegerField('height', validators=[DataRequired()])
    weight = IntegerField('weight', validators=[DataRequired()])
    age = IntegerField('age', validators=[DataRequired()])
    submit = SubmitField('ADD')

class CreateContactForm(FlaskForm):
    number = IntegerField('number', validators=[DataRequired()])
    name = StringField('name', validators=[DataRequired()])
    phone = StringField('phone', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    address = StringField('address', validators=[DataRequired()])
    submit = SubmitField('ADD')

class CreatePerformanceForm(FlaskForm):
    number = IntegerField('number', validators=[DataRequired()])
    min = IntegerField('min', validators=[DataRequired()])
    reb = IntegerField('reb', validators=[DataRequired()])
    pts = IntegerField('pts', validators=[DataRequired()])
    ast = IntegerField('ast', validators=[DataRequired()])
    stl = IntegerField('stl', validators=[DataRequired()])
    blk = IntegerField('blk', validators=[DataRequired()])
    to = IntegerField('to', validators=[DataRequired()])
    pf = IntegerField('pf', validators=[DataRequired()])
    submit = SubmitField('ADD')

class EditTalentForm(FlaskForm):
    number = IntegerField('number', validators=[DataRequired()])
    name = StringField('name', validators=[DataRequired()])
    img = StringField('img', validators=[DataRequired()])
    position = SelectField('position', choices = position_options)
    country = StringField('country', validators=[DataRequired()])
    height = IntegerField('height', validators=[DataRequired()])
    weight = IntegerField('weight', validators=[DataRequired()])
    age = IntegerField('age', validators=[DataRequired()])
    submit = SubmitField('UPDATE')

class EditContactForm(FlaskForm):
    number = IntegerField('number', validators=[DataRequired()])
    name = StringField('name', validators=[DataRequired()])
    phone = StringField('phone', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    address = StringField('address', validators=[DataRequired()])
    submit = SubmitField('UPDATE')

class EditPerformanceForm(FlaskForm):
    number = IntegerField('number', validators=[DataRequired()])
    min = IntegerField('min', validators=[DataRequired()])
    reb = IntegerField('reb', validators=[DataRequired()])
    pts = IntegerField('pts', validators=[DataRequired()])
    ast = IntegerField('ast', validators=[DataRequired()])
    stl = IntegerField('stl', validators=[DataRequired()])
    blk = IntegerField('blk', validators=[DataRequired()])
    to = IntegerField('to', validators=[DataRequired()])
    pf = IntegerField('pf', validators=[DataRequired()])
    submit = SubmitField('UPDATE')

class DeleteTalentForm(FlaskForm):
    confirm = BooleanField('ARE YOU SURE YOU WANT TO DELETE?', validators=[DataRequired()])
    submit = SubmitField('DELETE')


class CreateCommentForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    content = TextAreaField('COMMENT', validators=[DataRequired()])
    submit = SubmitField('POST')


class EditCommentForm(FlaskForm):
    content = TextAreaField('COMMENT', validators=[DataRequired()])
    submit = SubmitField('EDIT')
