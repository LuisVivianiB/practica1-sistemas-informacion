import hashlib
import sqlite3
import usersClass

from flask import Flask, render_template, request
import pandas as pd
import json
import plotly
import plotly.express as px
import requests
from flask_login import LoginManager


import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn import tree
from sklearn.datasets import load_iris
import graphviz

app = Flask(__name__)

login_manager = LoginManager(app)

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

@app.route('/index',methods=['GET','POST'])
@login_manager.user_loader
def login():
    con = sqlite3.connect('database.db')
    username = (request.form["username"])
    password = (request.accept_encodings["password"])
    UserParaLogin = pd.DataFrame(pd.read_sql("SELECT * FROM usuarios", con), columns=["nombre", "contrasena"])
    for user in UserParaLogin:
        if (user.nombre == username) and (usersClass.user.check_password(user,password)):
            return loginRet(1)
        else:
            return loginRet(0)

@app.route('/login',methods=['GET','POST'])
def loginRet(bool):
    if (bool):
        render_template('login.html', header="Has iniciado sesión")
    else:
        render_template('login.html', header="Error al iniciar sesión")


def crearData():
    usuariosTrain = open("users_IA_clases.json", "r")
    usuarios = json.load(usuariosTrain)

    usuariosApredecir = open("users_IA_predecir.json", "r")
    nuevosUsuarios = json.load(usuariosApredecir)

    phishing = pd.DataFrame(usuarios['usuarios'], columns=['emails_phishing_recibidos','emails_phishing_clicados', 'vulnerable'])
    phishing['emailsDivison']= phishing['emails_phishing_clicados'] / phishing['emails_phishing_recibidos']
    phishing = phishing.dropna()

    phishingNuevos = pd.DataFrame(nuevosUsuarios['usuarios'],columns=['emails_phishing_recibidos', 'emails_phishing_clicados'])
    phishingNuevos['emailsDivison'] = phishingNuevos['emails_phishing_clicados'] / phishingNuevos['emails_phishing_recibidos']
    phishingNuevos = phishingNuevos.dropna()
    userEmails_train = phishing['emailsDivison'][:-20].values.reshape(-1, 1)
    userEmails_test = phishingNuevos['emailsDivison'][-20:].values.reshape(-1, 1)

    userVulnerable_train = phishing['vulnerable'][:-20].values.reshape(-1, 1)
    userVulnerable_test = phishingNuevos['vulnerable'][-20:].values.reshape(-1, 1)

    return userEmails_train, userEmails_test, userVulnerable_train, userVulnerable_test

@app.route('/RegresionLineal', methods=['GET'])
def linearRegression():

    array=crearData()
    userEmails_train = array[0]
    userEmails_test = array[1]
    userVulnerable_train = array[2]
    userVulnerable_test = array[3]

    reg = LinearRegression()
    reg.fit(userEmails_train, userVulnerable_train)
    print(reg.coef_)
    userVulnerable_predict = reg.predict(userVulnerable_test)
    print("Mean squared error: %.2f" % mean_squared_error(userVulnerable_test, userVulnerable_predict))

    # Plot outputs
    print("pred:",userEmails_test)
    plt.scatter(userEmails_test.ravel(), userVulnerable_test, color="black")
    plt.plot(userEmails_test.ravel(), userVulnerable_predict, color="blue", linewidth=3)
    plt.xticks(())
    plt.yticks(())
    plt.show()

    return render_template('index.html')

@app.route('/DecisionTree',methods=['GET','POST'])
def DecisionTree():
    array = crearData()
    userEmails_train = array[0]
    userEmails_test = array[1]
    userVulnerable_train = array[2]
    userVulnerable_test = array[3]

    X, y = userEmails_train, userVulnerable_train
    # Predict
    clf_model = tree.DecisionTreeClassifier()
    clf_model.fit(X, y)






app.run()
