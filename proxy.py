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

@app.route("/map")
def map():
    return app.send_static_file('map.html')

@app.route("/stat_wifi")
def stat_wifi():
    return app.send_static_file('stat_wifi.html')

@app.route("/googleef86e8bbc6c2f64d.html")
def cenas():
    return app.send_static_file('googleef86e8bbc6c2f64d.html')

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

@app.route("/api/wifilog/marked/", methods = ['GET'])
def getWifiLogsMarkedJSON():
    print("called getWifiLogsMarkedJSON function")
    wifis = []
    try:
        marked = dbWiFi.wifiLogsMarked()
        non_marked = dbWiFi.wifiLogsNonMarked()
        print("success on getWifiLogsMarkedJSON")
        dict_m = {}
        for m in marked:
            if m["ssid"] not in dict_m:
                ab = [1,0]
                dict_m[m["ssid"]] = ab
            else:
                ab = dict_m[m["ssid"]]
                ab[0] = ab[0] + 1
                dict_m[m["ssid"]] = ab
            
            #print(m)
        for m in non_marked:
            if m["ssid"] not in dict_m:
                ab = [0,1]
                dict_m[m["ssid"]] = ab
            else:
                ab = dict_m[m["ssid"]]
                ab[1] = ab[1] + 1
                dict_m[m["ssid"]] = ab
        #print(dict_m)

        x = dict_m.keys()
        for a in x:
            print(a)
            ab = dict_m[a]
            if ab[0] == 0:
                res = 0
            else:
                res = ab[0]/(ab[0] + ab[1]) * 100
            l = [a, ab[0], ab[1], round(res,2)]
            print(l)
            wifis.append(l)

        #wifis.append(dict_m)
    except:
        wifis = []
        print("failure on getWifiLogsMarkedJSON")
    
    return {"wifis": wifis}

@app.route("/api/gpslog/", methods = ['GET'])
def getGPSLogsJSON():
    print("called getGPSLogsJSON function")

    try:
        gpss = dbGPS.allGPSLogsDICT()
        print("success on getGPSLogsJSON")
    except:
        gpss = []
        print("failure on getGPSLogsJSON")
    
    return {"gpss": gpss}

@app.route("/api/gpslog/marked/", methods = ['GET'])
def getGPSLogsMarkedJSON():
    print("called getGPSLogsMarkedJSON function")

    try:
        gpss = dbGPS.allGPSLogsMarkedDICT()
        print("success on getGPSLogsMarkedJSON")
    except:
        gpss = []
        print("failure on getGPSLogsMarkedJSON")
    
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