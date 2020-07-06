from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class BaseForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    submit = SubmitField('Отправить')

class NeedsForm(BaseForm):
    needs = StringField('Needs', validators=[DataRequired()])

class GiverForm(BaseForm):
    gift = StringField('Needs', validators=[DataRequired()])