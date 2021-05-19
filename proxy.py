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
    print("called getUsersJSON function")

    try:
        users = dbUser.allUsersDICT()
        print("success on getUsersJSON")
    except:
        users = []
        print("failure on getUsersJSON")

    return {"users": users}

@app.route("/api/usersinfected/", methods = ['GET'])
def getUsersInfectedJSON():
    print("called getUsersInfectedJSON function")

    try:
        usersinfected = dbUser.allUsersInfectedDICT()
        print("success om getUsersInfectedJSON")
    except:
        usersinfected = []
        print("failure on getUsersInfectedJSON")

    return {"usersinfected": usersinfected}

@app.route("/api/users/<int:idUser>/marked/", methods = ['UPDATE'])
def updateUsersMarkedJSON(idUser):
    print("called updateUsersMarkedJSON function")

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
        print("success on transformation dates to dicts")
    except:
        print("failure on transformation dates to dicts")

    try:
        dbGPS.changeMarked(idUser, date1, date2)
        print("success on marking gps logs")
    except:
        print("failure on marking gps logs")

    try:
        dbWiFi.changeMarked(idUser, date1, date2)
        print("success on marking wifi logs")
    except:
        print("failure on marking wifi logs")

    try:
        dbUser.newUserInfected(idUser, j["dia_inicio"], j["mes_inicio"], j["ano_inicio"], j["dia_fim"], j["mes_fim"], j["ano_fim"])
        print("success on creating new infected user")
    except:
        print("failure on creating new infected user")
        
    ret = "OK"
    return {"check": ret}

@app.route("/api/wifilog/", methods = ['GET'])
def getWifiLogsJSON():
    print("called getWifiLogsJSON function")

    try:
        wifis = dbWiFi.allWifiLogsDICT()
        print("success on getWifiLogsJSON")
    except:
        wifis = []
        print("failure on getWifiLogsJSON")
    
    return {"wifis": wifis}

@app.route("/api/gpslog/", methods = ['GET'])
def getGPSLogsJSON():
    print("called getGPSLogsJSON function")

    try:
        gpss = dbGPS.allGPSLogsDICT()
        print("success on getGPSLogsJSON")
    except:
        gpss = []
        print("success on getGPSLogsJSON")
    
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