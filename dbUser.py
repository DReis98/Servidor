from flask import *
from flaskXMLRPC import XMLRPCHandler

from os import path

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy import ForeignKey
from sqlalchemy import and_
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

    def toDictionary(self):
        return {"id": self.id, "username": self.username, "password": self.password}

class UserInfected(Base):
    __tablename__ = 'userinfected'
    id = Column(Integer, primary_key = True)
    id_user = Column(Integer)
    dia_inicio = Column(Integer)
    mes_inicio = Column(Integer)
    ano_inicio = Column(Integer)
    dia_fim = Column(Integer)
    mes_fim = Column(Integer)
    ano_fim = Column(Integer)

    def __repr__(self):
        return "<id: %d, id_user: %d, data inicio: %d/%d/%d, data fim: %d/%d/%d>" % (self.id, self.id_user, self.dia_inicio, self.mes_inicio, self.ano_inicio, self.dia_fim, self.mes_fim, self.ano_fim)

    def toDictionary(self):
        return {"id": self.id, "id_user": self.id_user, "dia_inicio": self.dia_inicio, "mes_inicio": self.mes_inicio, "ano_inicio": self.ano_inicio, "dia_fim": self.dia_fim, "mes_fim": self.mes_fim, "ano_fim": self.ano_fim}

# CREATE TABLES FOR THE DATA MODELS
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

app = Flask(__name__)
handler = XMLRPCHandler('apiUser')
handler.connect(app, '/apiUser')

# HANDLER FUNCTIONS

"""
Creates a new entry in UserInfected database.
Receives the parameters and returns the sequential id. In case of error, returns 0.
"""
@handler.register
def newUserInfected(id_user, dia_inicio, mes_inicio, ano_inicio, dia_fim, mes_fim, ano_fim):
    number = 0
    print("here 1")
    new = UserInfected(id_user = id_user, dia_inicio = dia_inicio, mes_inicio = mes_inicio, ano_inicio = ano_inicio, dia_fim = dia_fim, mes_fim = mes_fim, ano_fim = ano_fim)
    print("here 2")
    try:
        session.add(new)
        session.commit()
        number = new.id
        print("Added successfully") 
        print(new.__repr__())
        print()
        session.close()
    except:
        print("Failed adding userinfected")

    return number

"""
Creates a new entry in User database.
Receives the parameters and returns the sequential id. In case of error, returns 0.
"""
@handler.register
def newUser(username, password):
    number = 0

    newUser = User(username = username, password = password)
    try:
        session.add(newUser)
        session.commit()
        number = newUser.id
        print("Added successfully") 
        print(newUser.__repr__())
        print()
        session.close()
    except:
        print("Failed adding user")

    return number

"""
Looks if there is a certain username in the database
Returns the number of entries with that specific username. Must be 0 or 1
"""
@handler.register
def checkUserExists(username):
    print("called checkUserExists function")
    users = session.query(User).filter(User.username == username).all()
    session.close()
    count = 0
    for user in users:
        count = count + 1
    return count

"""
Looks if there is a certain username has a specific password
Returns the number of entries with that specific username and password. Must be 0 or 1
"""
@handler.register
def checkUserPassword(username, password):
    print("called checkUserPassword function")
    users = session.query(User).filter(and_(User.username == username, User.password == password)).all()
    session.close()
    count = 0
    for user in users:
        count = count + 1
    return count

"""
Looks if there is a certain username in the database
Returns the number of entries with that specific username. Must be 0 or 1
"""
@handler.register
def getIdUser(username):
    print("called getIdUser function")
    users = session.query(User).filter(User.username == username).first()
    id_user = 0
    try:
        id_user = users.id
    except:
        id_user = 0
        print("Except")
    session.close()
    return id_user

"""
Returns all the entries in the User database
"""
@handler.register
def allUsersDICT():
    print("called allUsersDICT function")
    users = session.query(User).all()
    session.close()
    retList = []
    for user in users:
        u = user.toDictionary()
        retList.append(u)

    return retList

"""
Returns all the entries in the UserInfected database
"""
@handler.register
def allUsersInfectedDICT():
    print("called allUsersInfectedDICT function")
    usersinfected = session.query(UserInfected).all()
    session.close()
    retList = []
    for user in usersinfected:
        u = user.toDictionary()
        retList.append(u)

    return retList

# OTHER FUNCTIONS

if __name__ == "__main__":
    app.run(host = '0.0.0.0', port = 8002, debug = True)