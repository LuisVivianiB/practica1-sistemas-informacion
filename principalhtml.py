import hashlib
import sqlite3

from flask import Flask, render_template, request
import pandas as pd
import json
import plotly
import plotly.express as px
import requests

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
    TopUsuariosCriticos = pd.DataFrame(pd.read_sql(
        "SELECT u.nombre, u.contrasena, e.phishing, e.cliclados FROM usuarios u join emails e on u.nombre=e.usuario",con), columns=["nombre", "contrasena", "phishing", "cliclados"])

    diccionario = open("commonPass.txt", "r")
    dicsplit = diccionario.read().split("\n")
    TopUsuariosCriticos['insegura'] = 0
    for passw in dicsplit:
        hash = hashlib.md5(passw.encode('utf-8')).hexdigest()
        TopUsuariosCriticos.loc[TopUsuariosCriticos.contrasena == str(hash), 'insegura'] = 1


    TopUsuariosCriticos.loc[TopUsuariosCriticos.insegura == 1, 'probCritico'] = TopUsuariosCriticos["cliclados"] / \
                                                                                TopUsuariosCriticos["phishing"]
    Top = TopUsuariosCriticos.sort_values(by=['probCritico'], ascending=False)
    Top = Top[Top['insegura'] == 1]


    Top = Top.dropna(axis=1)
    filtrado = Top
    if request.method == 'POST':
        submit = (request.form["text"])
        Cincuentapor = (request.form["porcentaje"])
        Top.loc[filtrado.probCritico >= 0.5, 'cincuenta'] = 0
        Top.loc[filtrado.probCritico < 0.5, 'cincuenta'] = 1
        if (submit.isdigit()):
            if(int(Cincuentapor)==0):
                filtrado = Top[Top["cincuenta"]==0]
            elif(int(Cincuentapor)==1):
                filtrado = Top[Top["cincuenta"] == 1]

            filtrado = filtrado.head(int(submit))


    fig = px.bar(filtrado, x="nombre", y="probCritico")

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    header = "Top Usuarios Criticos"
    return render_template('TopUsuariosCriticos.html', graphJSON=graphJSON, header=header)

@app.route('/TenVulTiempoReal',methods=['GET'])
def TenVulTiempoReal():
    url = "https://cve.circl.lu/api/last"
    response = requests.get(url).text
    data = pd.DataFrame(pd.read_json(response), columns=['id', 'cvss'])
    data = data.head(10)
    fig = px.bar(data, x="id", y="cvss")
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('TenVulTiempoReal.html', graphJSON=graphJSON, header="Top 10 Vulnerabilidades Tiempo Real")






app.run()
