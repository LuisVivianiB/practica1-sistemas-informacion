import sqlite3

from flask import Flask, render_template, request
import pandas as pd
import json
import plotly
import plotly.express as px

# from SQLite import con

app = Flask(__name__)


# con = sqlite3.connect('templates/database.db')

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/WebVulnerable', methods=['POST', 'GET'])
def WebVulnerable():
    con = sqlite3.connect('database.db')
    TopWebVulnerable = pd.DataFrame(pd.read_sql("SELECT * FROM legal", con),columns=["url", "cookies", "aviso", "proteccion_de_datos"])
    TopWebVulnerable["nivelDeDesactualizacion"] = TopWebVulnerable["cookies"] + TopWebVulnerable["aviso"] + TopWebVulnerable["proteccion_de_datos"]

    TopWebVulnerable = TopWebVulnerable.dropna(axis=1)
    TopWebVulnerable.sort_values(by=["nivelDeDesactualizacion"], ascending=False, inplace=True)
    if request.method == 'POST':

        submit = (request.form["text"])
        if(submit.isdigit()):
            TopWebVulnerable = TopWebVulnerable.head(int(submit))


    fig = px.bar(TopWebVulnerable, x="url", y="nivelDeDesactualizacion")

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    header = "Top Webs Vulnerables"

    return render_template('WebVulnerable.html', graphJSON=graphJSON, header=header)


@app.route('/TopUsuariosCriticos')
def chart2():
    df = pd.DataFrame({
        "Vegetables": ["Lettuce", "Cauliflower", "Carrots", "Lettuce", "Cauliflower", "Carrots"],
        "Amount": [10, 15, 8, 5, 14, 25],
        "City": ["London", "London", "London", "Madrid", "Madrid", "Madrid"]
    })

    fig = px.bar(df, x="Vegetables", y="Amount", color="City", barmode="stack")

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    header = "Vegetables in Europe"
    description = """
    The rumor that vegetarians are having a hard time in London and Madrid can probably not be
    explained by this chart.
    """
    return render_template('chart2.html', graphJSON=graphJSON, header=header, description=description)


app.run()
