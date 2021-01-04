from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, scoped_session

from datetime import datetime
from sqlalchemy.orm import sessionmaker
from os import path


#SLQ access layer initialization
DATABASE_FILE = "logs.sqlite"
db_exists = False
if path.exists(DATABASE_FILE):
    db_exists = True
    print("\t database already exists")

engine = create_engine('sqlite:///%s'%(DATABASE_FILE), echo=False) #echo = True shows all SQL calls

Base = declarative_base()



#Declaration of data
  


class Logs(Base):
    __tablename__ = 'Logs'
    id = Column(Integer, primary_key=True)
    date = Column(String)     
    description = Column(String)
    
    def __repr__(self):
        return "<Logs (id=%d date='%s', description='%s'>" % (
                                self.id, self.date, self.description)
    def to_dictionary(self):
        return {"id": self.id, "date": self.date, "description": self.description}
    

Base.metadata.create_all(engine) #Create tables for the data models

Session = sessionmaker(bind=engine)
session = scoped_session(Session)


def newLog(description):
    now = datetime.now()
    log = Logs(description = description, date = now.strftime("%d/%m/%Y %H:%M:%S"))
    try:
        session.add(log)
        session.commit()
        print(log.id)
        session.close()
        return log.id
    except:
        return None
    
def listLogs():
    return session.query(Logs).all()
    session.close()

def listLogsDICT():
    ret_list = []
    ll = listLogs()
    for l in ll:
        l_ = l.to_dictionary()
        ret_list.append(l_)
    return ret_list


if __name__ == "__main__":
    pass