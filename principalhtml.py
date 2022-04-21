import hashlib
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


@app.route('/TopUsuariosCriticos',methods=['POST', 'GET'])
def TopUsuariosCriticos():
    con = sqlite3.connect('database.db')
    TopUsuariosCriticos =pd.DataFrame(pd.read_sql("SELECT u.nombre u.contrasena e.phishing e.cliclados FROM usuarios u join emails e on u.nombre=e.usuario",con),columns=["nombre", "contrasena", "phishing", "cliclados"])
    TopUsuariosCriticosContrasenaVulnerada =pd.DataFrame(columns=["nombre", "phishing", "cliclados"])
    diccionario = open("commonPasswords.txt", "r")
    dicsplit = diccionario.read().split("\n")
    for i in TopUsuariosCriticos["contrasena"]:
        for passw in dicsplit:
            hash = hashlib.md5(passw)
            if (passw == str(hash)):
                TopUsuariosCriticosContrasenaVulnerada.loc[len(TopUsuariosCriticos.index)] = TopUsuariosCriticos.loc [i, ['nombre', 'phishing', 'cliclados']]




    TopUsuariosCriticosContrasenaVulnerada = TopUsuariosCriticosContrasenaVulnerada.dropna(axis=1)
    #if request.method == 'POST':

        #submit = (request.form["text"])
        #if (submit.isdigit()):
            #TopUsuariosCriticosContrasenaVulnerada = TopUsuariosCriticosContrasenaVulnerada.head(int(submit))

    fig = px.bar(TopUsuariosCriticosContrasenaVulnerada, x="nombre", y="phishing")

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    header = "Top Usuarios Criticos"
    return render_template('TopUsuariosCriticos.html', graphJSON=graphJSON, header=header)


app.run()
