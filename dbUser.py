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
DATABASE_FILE = "dbUser.sqlite"
db_exists = False
if path.exists(DATABASE_FILE):
    db_exists = True

engine = create_engine('sqlite:///%s'%(DATABASE_FILE), echo = False)

Base = declarative_base()

# DECLARATION OF CLASSES
class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key = True)
    username = Column(String)
    password = Column(String)

    def __repr__(self):
        return "<id: %d, username: %s, password: %s>" % (self.id, self.username, self.password)

# CREATE TABLES FOR THE DATA MODELS
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

app = Flask(__name__)
handler = XMLRPCHandler('apiUser')
handler.connect(app, '/apiUser')

# HANDLER FUNCTIONS

"""
Creates a new entry in User database.
Receives the parameters and returns the sequential id. In case of error, returns 0.
"""
@handler.register
def newUser(username, password):
    print("called newUser function")
    number = 0

    newUSer = User(username = username, password = password)
    try:
        session.add(newUSer)
        session.commit()
        number = newUSer.id
        session.close()
        print("Added successfully") 
    except:
        print("Failed adding user")

    return number

# OTHER FUNCTIONS

if __name__ == "__main__":
    app.run(host = '0.0.0.0', port = 8002, debug = True)