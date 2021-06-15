from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
from markupsafe import Markup


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    host = StringField('Host/Server', validators=[DataRequired()])
    db = StringField('Database', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class ConnectForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    server = StringField('Host/Server', validators=[DataRequired()])
    db = StringField('Database', validators=[DataRequired()])
    submit = SubmitField('Connect')


class ConvertForm(FlaskForm):
    text = TextAreaField('Text', render_kw={"rows": 20, "cols": 60})
    view_sql = SubmitField('View SQL')
    execute_sql = SubmitField('Execute SQL')