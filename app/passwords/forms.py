from flask_wtf import Form
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired, Length


class PasswordForm(Form):
    title = StringField('Title', validators=[DataRequired(), Length(1, 100)])
    username = StringField('Username/Login', validators=[Length(0, 50)])
    password = StringField('Password', validators=[Length(0, 50)])
    website = StringField('Website (URL)', validators=[Length(0, 100)])
    description = StringField('Description', validators=[Length(0, 200)])
    submit = SubmitField('Submit')