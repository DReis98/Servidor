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
DATABASE_FILE = "dbGPS.sqlite"
db_exists = False
if path.exists(DATABASE_FILE):
    db_exists = True

engine = create_engine('sqlite:///%s'%(DATABASE_FILE), echo = False)

Base = declarative_base()

# DECLARATION OF CLASSES
class GPSLog(Base):
    __tablename__ = 'gpslog'
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
    lat = Column(Float)
    lon = Column(Float)
    marked = Column(Integer)

    def __repr__(self):
        return "<id: %d, id_user: %d, data: %s, data_dia: %d, data_mes: %d, data_ano: %d, hora: %s, hora_hora: %d, hora_minuto: %d, hora_segundo: %d, lat: %f, lon: %f, marked: %d>" % (self.id, self.id_user, self.data, self.data_dia, self.data_mes, self.data_ano, self.hora, self.hora_hora, self.hora_minuto, self.hora_segundo, self.lat, self.lon, self.marked)

    def toDictionary(self):
        return {"id": self.id, "id_user": self.id_user, "data": self.data, "hora": self.hora, "lat": self.lat, "lon": self.lon, "marked": self.marked}


# CREATE TABLES FOR THE DATA MODELS
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

app = Flask(__name__)
handler = XMLRPCHandler('apiGPSLog')
handler.connect(app, '/apiGPSLog')

# HANDLER FUNCTIONS

"""
Creates a new entry in GPSLog database.
Receives the parameters and returns the sequential id. In case of error, returns 0.
"""
@handler.register
def newGPSLog(id_user, data, hora, lat, lon):
    print("called newGPSLog function")

    number = 0

    # data e hora 
    try:
        d = data.split("-")
        data_dia = int(d[0])
        data_mes = int(d[1])
        data_ano = int(d[2])

        h = hora.split(":")
        hora_hora = int(h[0])
        hora_minuto = int(h[1])
        hora_segundo = int(h[2])

        print("success on get date and time from dict")
    except:
        print("failure on get date and time from dict")

    try:
        newGPS = GPSLog(id_user = id_user, data = data, data_dia = data_dia, data_mes = data_mes, data_ano = data_ano, hora = hora, hora_hora = hora_hora, hora_minuto = hora_minuto, hora_segundo = hora_segundo, lat = lat, lon = lon, marked = 0)
        session.add(newGPS)
        session.commit()
        number = newGPS.id
        session.close()  
        print("success on newGPSLog")  
    except:
        print("failure on newGPSLog")  

    return number

"""
Returns all the entries in the WiFiLog database
"""
@handler.register
def allGPSLogsDICT():
    print("called allGPSLogsDICT function")

    try:
        gpss = session.query(GPSLog).all()
        session.close()
        retList = []
        for gps in gpss:
            g = gps.toDictionary()
            retList.append(g)
        print("success on allGPSLogsDICT")
    except:
        print("failure on allGPSLogsDICT")

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
            gpss = session.query(GPSLog).filter(and_(GPSLog.id_user == id, GPSLog.data_mes == date["month"], GPSLog.data_dia == date["day"], GPSLog.data_ano == date["year"])).all()
            for gps in gpss:
                gps.marked = 1
            session.commit()
            session.close()   
            print("success on changeMarked") 
        except:
            print("failure on changeMarked") 
        
        date = nextDay(date)
        compDates = compareDates(date, date2)

# OTHER FUNCTIONS

if __name__ == "__main__":
    app.run(host = '0.0.0.0', port = 8000, debug = True)