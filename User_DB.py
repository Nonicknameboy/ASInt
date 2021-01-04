from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, scoped_session

import datetime
from sqlalchemy.orm import sessionmaker
from os import path
import datetime


#SLQ access layer initialization
DATABASE_FILE = "users.sqlite"
db_exists = False
if path.exists(DATABASE_FILE):
    db_exists = True
    print("\t database already exists")

engine = create_engine('sqlite:///%s'%(DATABASE_FILE), echo=False) #echo = True shows all SQL calls

Base = declarative_base()

admins = ["ist14028", "ist425426", "ist425484"]


#admin_list = [{"user_id": "ist14028", "name": "João Silva", "admin": 1}, 
#{"user_id": "ist425426", "name": "Manuel Domingues", "admin": 1}, 
#{"user_id": "ist425484", "name": "Simão Soares", "admin": 1}]


# daqui para cima é igual? (menos o DATABASE_FILE) ---------------------------------------


#Declaration of data
  


class Users(Base):
    __tablename__ = 'Users'
    user_id = Column(String, primary_key=True)
    name = Column(String)     
    admin = Column(Integer)
    
    def __repr__(self):
        return "<User (id=%s name='%s', admin='%d'>" % (
                                self.user_id, self.name, self.admin)
    def to_dictionary(self):
        return {"user_id": self.user_id, "name": self.name, "admin": self.admin}
    

Base.metadata.create_all(engine) #Create tables for the data models

Session = sessionmaker(bind=engine)
session = scoped_session(Session)


# função que preenche database dos users com os admins definidos na list de dicts
#def populateAdmins(admin_list):


def newUser(name,uID):
    ad = uID in admins
    if not ad:                                  # se nao for admin
        if getUser(uID) == None:                # se for nao admin e n existe
            u = Users(name = name, user_id = uID, admin=0)
            try:
                session.add(u)
                session.commit()
                print(u.user_id)
                print("User (not admin) added")
                session.close()
                return u.to_dictionary()
            except:
                return None
        else:                                    # se for nao admin e ja existe             
            print("User (not admin) already exists")
            u = getUser(uID)
            return u.user_id
    else:                                         # se for admin
        if getUser(uID) == None:                  # se for admin e n existe
            u = Users(name = name, user_id = uID, admin=1)
            try:
                session.add(u)
                session.commit()
                print(u.user_id)
                print("User (admin) added")
                session.close()
                return u.to_dictionary()
            except:
                return None
        else:                                    # se for admin e n existe
            print("User (admin) already exists")
            u = getUser(uID)
            return u.user_id
    
def getUserDICT(userID):
    return getUser(userID).to_dictionary()
    
def getUser(id):
    U =  session.query(Users).filter(Users.user_id==id).first()
    session.close()
    return U



if __name__ == "__main__":
    pass