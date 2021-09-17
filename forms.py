from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, URL


class SubmitPlayers(FlaskForm):
    player_1 = StringField("Player 1", validators=[DataRequired()])
    player_2 = StringField("Player 2", validators=[DataRequired()])
    submit = SubmitField("Get Chart")
