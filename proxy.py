import xmlrpc.server

from sqlalchemy.sql.expression import table

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
def map_google():
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

@app.route("/api/userspossibleinfected/", methods = ['GET'])
def getUsersPossibleInfectedJSON():
    print("called getUsersPossibleInfectedJSON function")

    try:
        userspossibleinfected = dbUser.allUsersPossibleInfectedDICT()
        print("success on getUsersPossibleInfectedJSON")
    except:
        userspossibleinfected = []
        print("failure on getUsersPossibleInfectedJSON")

    return {"userspossibleinfected": userspossibleinfected}

@app.route("/api/users/<int:idUser>/marked/", methods = ['UPDATE'])
def updateUsersMarkedJSON(idUser):
    print("called updateUsersMarkedJSON function")

    j = request.get_json()
    date1 = {}
    date2 = {}
    # put data into dictionaries
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

    # update gps table
    try:
        dbGPS.changeMarked(idUser, date1, date2)
        print("success on marking gps logs")
    except:
        print("failure on marking gps logs")

    # update wifi table
    try:
        dbWiFi.changeMarked(idUser, date1, date2)
        print("success on marking wifi logs")
    except:
        print("failure on marking wifi logs")

    # new entry on usersinfected table
    try:
        dbUser.newUserInfected(idUser, j["dia_inicio"], j["mes_inicio"], j["ano_inicio"], j["dia_fim"], j["mes_fim"], j["ano_fim"])
        print("success on creating new infected user")
    except:
        print("failure on creating new infected user")
    
    # look for users GPS
    try:
        tableGPS = dbGPS.usersPossibleInfectedGPS(idUser, date1, date2)
        print("success on searching for new users infected gps")
    except:
        tableGPS = []
        print("failure on searching for new users infected gps")
    
    print("Table GPS:")
    print(tableGPS)

    try:
        for a in tableGPS:
            dbUser.updateOc(a, 0)
        print("success on updating gps")
    except:
        print("failure on updating gps")

    # look for users WiFi
    try:
        tableWiFi = dbWiFi.usersPossibleInfectedWiFi(idUser, date1, date2)
        print("success on searching for new users infected wifi")
    except:
        tableWiFi = []
        print("failure on searching for new users infected wifi")
    
    print("Table WiFi:")
    print(tableWiFi)

    try:
        for a in tableWiFi:
            dbUser.updateOc(a, 1)
        print("success on updating wifi")
    except:
        print("failure on updating wifi")

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

if __name__ == "__main__":
    app.run(host = '0.0.0.0', port = 3002, debug = True)