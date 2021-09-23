from flask import Flask, render_template, redirect, url_for, flash, abort, request
from flask_bootstrap import Bootstrap
from forms import SubmitPlayers
from mplsoccer import FontManager
from chart import chart_maker
import pandas as pd
import random
import base64

URL4 = 'https://github.com/googlefonts/roboto/blob/main/src/hinted/Roboto-Thin.ttf?raw=true'
robotto_thin = FontManager(URL4)
URL5 = 'https://github.com/googlefonts/roboto/blob/main/src/hinted/Roboto-Regular.ttf?raw=true'
robotto_regular = FontManager(URL5)
URL6 = 'https://github.com/googlefonts/roboto/blob/main/src/hinted/Roboto-Bold.ttf?raw=true'
robotto_bold = FontManager(URL6)

# read in data
df = pd.read_csv("data.csv")
df["Player"] = df["Player"].str.split("\\", expand=True)[0]

# filter data to only forwards that have played more than 2 full games
df = df[df["Pos"].str.contains("FW")]
df = df[df["90s"] >= 2.0]

# replace NaNs with 0 (contains NaNs where there would be a zero divide e.g. goals per shot on target)
df = df.fillna(0)

players = df["Player"].unique()


app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
Bootstrap(app)


@app.route('/', methods=['GET', 'POST'])
def home():
    random_player_1 = random.choice(players)
    random_player_2 = random.choice(players)
    while random_player_1 == random_player_2:
        random_player_2 = random.choice(players)
    form = SubmitPlayers(
        player_1=random_player_1,
        player_2=random_player_2
    )
    if form.validate_on_submit():
        player_1 = form.player_1.data
        player_2 = form.player_2.data
        try:
            img = chart_maker(player_1, player_2, df, robotto_thin, robotto_regular, robotto_bold)

            # convert to bases64
            data = img.read()  # get data from file (BytesIO)
            data = base64.b64encode(data)  # convert to base64 as bytes
            data = data.decode()  # convert bytes to string

            return render_template("result.html", data=data)
        except IndexError:
            flash(f"Player(s) not in list", 'info')
            return render_template("index.html", form=form)
    return render_template("index.html", form=form)


@app.route("/pca-2")
def pca2():
    return render_template("2_components.html")


@app.route("/pca-3")
def pca3():
    return render_template("3_components.html")


if __name__ == "__main__":
    app.run()
