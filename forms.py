from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, SelectField
from wtforms.validators import DataRequired, URL
import pandas as pd


# read in data
# df = pd.read_csv("data.csv")
df = pd.read_html("https://fbref.com/en/comps/Big5/shooting/players/Big-5-European-Leagues-Stats")[0]
cols_temp = [row[1] for row in df.columns]
df.columns = cols_temp
df = df[df["Comp"] == "eng Premier League"]
for col in df.columns[8:-1]:
    df[col] = pd.to_numeric(df[col])
index_names = df[df['Player'] == 'Mason Greenwood'].index
df.drop(index_names, inplace=True)
df["Player"] = df["Player"].str.split("\\", expand=True)[0]

# filter data to only forwards that have played more than 2 full games
df = df[df["Pos"].str.contains("FW")]
df = df[df["90s"] >= 2.0]

# replace NaNs with 0 (contains NaNs where there would be a zero divide e.g. goals per shot on target)
df = df.fillna(0)

players = df["Player"].unique()


class SubmitPlayers(FlaskForm):
    player_1 = SelectField("Player 1", choices=players)
    player_2 = SelectField("Player 2", choices=players)
    submit = SubmitField("Get Chart")
