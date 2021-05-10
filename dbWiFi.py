from flask import *
from flaskXMLRPC import XMLRPCHandler

from dates import *

from os import path

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy import ForeignKey
from sqlalchemy import and_
from sqlalchemy.orm import relationship, scoped_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# SQL access layer initialization
DATABASE_FILE = "dbWiFi.sqlite"
db_exists = False
if path.exists(DATABASE_FILE):
    db_exists = True

engine = create_engine('sqlite:///%s'%(DATABASE_FILE), echo = False)

Base = declarative_base()

# DECLARATION OF CLASSES
class WiFiLog(Base):
    __tablename__ = 'wifilog'
    id = Column(Integer, primary_key = True)
    id_user = Column(Integer)
    data = Column(String)
    data_dia = Column(Integer)
    data_mes = Column(Integer)
    data_ano = Column(Integer)
    hora = Column(String)
    hora_hora = Column(Integer)
    hora_minuto = Column(Integer)
    hora_segundo = Column(Integer)
    ssid = Column(String)
    marked = Column(Integer)

    def __repr__(self):
        return "<id: %d, id_user: %d, data: %s, data_dia: %d, data_mes: %d, data_ano: %d, hora: %s, hora_hora: %d, hora_minuto: %d, hora_segundo: %d, ssid: %s, marked: %d>" % (self.id, self.id_user, self.data, self.data_dia, self.data_mes, self.data_ano, self.hora, self.hora_hora, self.hora_minuto, self.hora_segundo, self.ssid, self.marked)

    def toDictionary(self):
        return {"id": self.id, "id_user": self.id_user, "data": self.data, "hora": self.hora, "ssid": self.ssid, "marked": self.marked}

# CREATE TABLES FOR THE DATA MODELS
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

app = Flask(__name__)
handler = XMLRPCHandler('apiWiFiLog')
handler.connect(app, '/apiWiFiLog')

# HANDLER FUNCTIONS

"""
Creates a new entry in WiFiLog database.
Receives the parameters and returns the sequential id. In case of error, returns 0.
"""
@handler.register
def newWiFiLog(id_user, data, hora, ssid):
    number = 0

    # data e hora
    d = data.split("-")
    data_dia = int(d[0])
    data_mes = int(d[1])
    data_ano = int(d[2])

    h = hora.split(":")
    hora_hora = int(h[0])
    hora_minuto = int(h[1])
    hora_segundo = int(h[2])

    newWiFi = WiFiLog(id_user = id_user, data = data, data_dia = data_dia, data_mes = data_mes, data_ano = data_ano, hora = hora, hora_hora = hora_hora, hora_minuto = hora_minuto, hora_segundo = hora_segundo, ssid = ssid, marked = 0)
    try:
        session.add(newWiFi)
        session.commit()
        number = newWiFi.id
        print("Added successfully") 
        print(newWiFi.__repr__())
        print()
        session.close()
    except:
        print("Failed adding wifi log")

    return number

"""
Returns all the entries in the WiFiLog database
"""
@handler.register
def allWifiLogsDICT():
    print("called allWifiLogsDICT function")
    wifis = session.query(WiFiLog).all()
    session.close()
    retList = []
    for wifi in wifis:
        w = wifi.toDictionary()
        retList.append(w)

    return retList

"""
Change marked column
"""
@handler.register
def changeMarked(id, date1, date2):
    print("called changeMarked function")
    date = date1
    compDates = compareDates(date1, date2)
    
    while compDates == 1:
        try:
            wifis = session.query(WiFiLog).filter(and_(WiFiLog.id_user == id, WiFiLog.data_mes == date["month"], WiFiLog.data_dia == date["day"], WiFiLog.data_ano == date["year"])).all()
            for wifi in wifis:
                wifi.marked = 1
            session.commit()
            print("Changed successfully") 
            session.close()   
        except:
            print("Failed changing wifilog marked")
        
        date = nextDay(date)
        compDates = compareDates(date, date2)

# OTHER FUNCTIONS

if __name__ == "__main__":
    app.run(host = '0.0.0.0', port = 8001, debug = True)