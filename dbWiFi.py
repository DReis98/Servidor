from flask import *
from flaskXMLRPC import XMLRPCHandler

from os import path

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, scoped_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# SQL access layer initialization
DATABASE_FILE = "dbWiFi.sqlite"
db_exists = False
if path.exists(DATABASE_FILE):
    db_exists = True

print(db_exists)

engine = create_engine('sqlite:///%s'%(DATABASE_FILE), echo = False)

Base = declarative_base()

# DECLARATION OF CLASSES
class WiFiLog(Base):
    __tablename__ = 'wifilog'
    id = Column(Integer, primary_key = True)
    id_user = Column(String)
    data = Column(String)
    hora = Column(String)
    ssid = Column(String)

    def __repr__(self):
        return "<id: %d, id_user: %s, data: %s, hora: %s, ssid: %s>" % (self.id, self.id_user, self.data, self.hora, self.ssid)

# CREATE TABLES FOR THE DATA MODELS
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

app = Flask(__name__)
handler = XMLRPCHandler('apiWiFiLog')
handler.connect(app, '/apiWiFiLog')

# HANDLER FUNCTIONS
@handler.register
def newWiFiLog(id_user, data, hora, ssid):
    print("called newWiFiLog function")
    number = 0

    newWiFi = WiFiLog(id_user = id_user, data = data, hora = hora, ssid = ssid)
    try:
        session.add(newWiFi)
        session.commit()
        number = newWiFi.id
        session.close()
        print("Added successfully") 
    except:
        print("Failed adding wifi log")

    return number

# OTHER FUNCTIONS

if __name__ == "__main__":
    app.run(host = '0.0.0.0', port = 8001, debug = True)