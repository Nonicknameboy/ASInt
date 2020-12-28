from xmlrpc.client import Boolean
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


# daqui para cima é igual? (menos o DATABASE_FILE) ---------------------------------------


#Declaration of data

class User(Base):
    __tablename__ = 'Users'
    user_id = Column(Integer, primary_key=True)
    name = Column(String)     
    admin = Column(Boolean)
    
    def __repr__(self):
        return "<User (id=%d name='%s', admin='%r'>" % (
                                self.user_id, self.name, self.admin)
    def to_dictionary(self):
        return {"user_id": self.user_id, "name": self.name, "admin": self.admin}
    