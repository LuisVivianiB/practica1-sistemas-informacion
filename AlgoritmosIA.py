
import sqlite3
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import json
from matplotlib import pyplot as plt
from sklearn import tree
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, accuracy_score


def crearData():
    usuariosTrain = open("users_IA_clases.json", "r")
    usuarios = json.load(usuariosTrain)

    phishing = pd.DataFrame(usuarios['usuarios'],
                            columns=['emails_phishing_recibidos', 'emails_phishing_clicados', 'vulnerable'])
    phishing['emailsDivison'] = phishing['emails_phishing_clicados'] / phishing['emails_phishing_recibidos']
    phishing = phishing.dropna()

    userEmails_train = phishing['emailsDivison'][:-6].values.reshape(-1, 1)

    userVulnerable_train = phishing['vulnerable'][:-6].values.reshape(-1, 1)

    userEmails_test = phishing['emailsDivison'][-24:].values.reshape(-1, 1)

    userVulnerable_test = phishing['vulnerable'][-24:].values.reshape(-1, 1)

    return userEmails_train, userVulnerable_train, userEmails_test, userVulnerable_test


def linearRegression():
    datos = crearData()
    userEmails_train = datos[0]
    userVulnerable_train = datos[1]
    userEmails_test = datos[2]
    userVulnerable_test = datos[3]

    regr = LinearRegression()
    regr.fit(userEmails_train, userVulnerable_train)
    prediccion = regr.predict(userVulnerable_test)

    for i in range(len(prediccion)):
        if (prediccion[i] < 0.5):
            prediccion[i] = 0
        else:
            prediccion[i] = 1

    print("Mean squared error: %.2f" % mean_squared_error(userEmails_test,prediccion))
    print("pred:", userVulnerable_test)
    plt.scatter(userEmails_test.ravel(), userVulnerable_test, color="black")
    plt.plot(userVulnerable_test.ravel(), prediccion, color="blue", linewidth=3)
    plt.xticks(())
    plt.yticks(())
    plt.show()


def DecisionTree():
    array = crearData()
    userEmails_train = array[0]
    userVulnerable_train = array[1]

    regr = tree.DecisionTreeClassifier()
    regr.fit(userEmails_train, userVulnerable_train)

    tree.plot_tree(regr, filled=True, fontsize=10, rounded=True, precision=2, proportion=False)
    plt.show()


def RandomForest():

    array = crearData()
    userEmails_train = array[0]
    userVulnerable_train = array[1]

    clf = RandomForestClassifier(max_depth=2, random_state=0, n_estimators=10)
    clf.fit(userEmails_train, userVulnerable_train)
    print(str(userEmails_train[0]) + " " + str(userVulnerable_train[0]))
    print(clf.predict([userEmails_train[0]]))
    for i in range(len(clf.estimators_)):
        estimator = clf.estimators_[i]
        tree.plot_tree(estimator, filled=True, fontsize=10, rounded=True, precision=2, proportion=False)
        plt.show()

con = sqlite3.connect('database.db')

#linearRegression()
#DecisionTree()
RandomForest()
