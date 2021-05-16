import xmlrpc.server

from dates import *

from flask import Flask, render_template, request

from xmlrpc import client


app = Flask(__name__)

dbGPS = client.ServerProxy("http://127.0.0.1:8000/apiGPSLog")
dbWiFi = client.ServerProxy("http://127.0.0.1:8001/apiWiFiLog")
dbUser = client.ServerProxy("http://127.0.0.1:8002/apiUser")

# ENDPOINTS
@app.route("/")
def main():
    return app.send_static_file('main_page.html')

@app.route("/gps")
def gps():
    return app.send_static_file('logs_gps.html')

@app.route("/wifi")
def wifi():
    return app.send_static_file('logs_wifi.html')

@app.route("/users")
def users():
    return app.send_static_file('users.html')

@app.route("/medical")
def medical():
    return app.send_static_file('medical.html')

# ENDPOINTS API
@app.route("/api/users/", methods = ['GET'])
def getUsersJSON():
    try:
        users = dbUser.allUsersDICT()
    except:
        users = []
    return {"users": users}

@app.route("/api/usersinfected/", methods = ['GET'])
def getUsersInfectedJSON():
    try:
        usersinfected = dbUser.allUsersInfectedDICT()
    except:
        usersinfected = []
    return {"usersinfected": usersinfected}

@app.route("/api/users/<int:idUser>/marked/", methods = ['UPDATE'])
def updateUsersMarkedJSON(idUser):
    print("Called updateUsersMarkedJSON")
    j = request.get_json()
    date1 = {}
    date2 = {}
    try:
        date1["day"] = j["dia_inicio"]
        date1["month"] = j["mes_inicio"]
        date1["year"] = j["ano_inicio"]
        date2["day"] = j["dia_fim"]
        date2["month"] = j["mes_fim"]
        date2["year"] = j["ano_fim"]
        dbGPS.changeMarked(idUser, date1, date2)
        dbWiFi.changeMarked(idUser, date1, date2)   
    except:
        print("Failed changing Marked")

    try:
        dbUser.newUserInfected(idUser, j["dia_inicio"], j["mes_inicio"], j["ano_inicio"], j["dia_fim"], j["mes_fim"], j["ano_fim"])
    except:
        print("Failed new user infected")
        
    ret = "OK"
    return {"check":ret}

@app.route("/api/wifilog/", methods = ['GET'])
def getWifiLogsJSON():
    try:
        wifis = dbWiFi.allWifiLogsDICT()
    except:
        wifis = []
    return {"wifis": wifis}

@app.route("/api/gpslog/", methods = ['GET'])
def getGPSLogsJSON():
    try:
        gpss = dbGPS.allGPSLogsDICT()
    except:
        gpss = []
    return {"gpss": gpss}

#######

@app.route("/random")
def index():
    return render_template("index.html")

@app.route("/motivation")
def motivation():
    return render_template("motivation.html")

if __name__ == "__main__":
    app.run(host = '0.0.0.0', port = 3002, debug = True)