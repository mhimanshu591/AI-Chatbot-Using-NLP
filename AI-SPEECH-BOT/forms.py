from wtforms import StringField, PasswordField, SubmitField, Form
from wtforms.validators import DataRequired, Regexp, ValidationError


class LoginForm(Form):  # created login form with validator....
    username = StringField(label="User Name", validators=[DataRequired()])
    password = PasswordField(label="Password",validators=[DataRequired()])
    submit = SubmitField("Login")