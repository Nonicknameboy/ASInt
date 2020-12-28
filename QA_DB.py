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
DATABASE_FILE = "questions_answers.sqlite"
db_exists = False
if path.exists(DATABASE_FILE):
    db_exists = True
    print("\t database already exists")

engine = create_engine('sqlite:///%s'%(DATABASE_FILE), echo=False) #echo = True shows all SQL calls

Base = declarative_base()


# daqui para cima é igual? (menos o DATABASE_FILE) ---------------------------------------


#Declaration of data

class Question(Base):
    __tablename__ = 'Question'
    video_id = Column(Integer, primary_key=True)    
    id = Column(Integer, primary_key=True)
    description = Column(String)
    time = Column(Integer)
    
    #video_id = Column(Integer, ForeignKey('YTVideo.id')) 
    #YTVideo = relationship("YTVideo", back_populates="questions")
    
    answers = relationship("Answer", back_populates="question")
    
    def __repr__(self):
        return "<Question (id=%d Description='%s', time='%d', videoID=%d>" % (
                                self.id, self.description, self.time, self.video_id)
    def to_dictionary(self):
        return {"question_id": self.id, "description": self.description, "time": self.time, "video":self.video_id}
    

class Answer(Base):
    __tablename__ = 'Answer'
    id = Column(Integer, primary_key=True)
    description = Column(String)
    
    question_id = Column(Integer, ForeignKey('Question.id')) 
    question = relationship("Question", back_populates="answers")
    
    def __repr__(self):
        return "<Answer (id=%d Description='%s', questionID=%d>" % (
                                self.id, self.description,self.question_id)
    def to_dictionary(self):
        return {"answer_id": self.id, "description": self.description, "question":self.question_id}
    


Base.metadata.create_all(engine) #Create tables for the data models

Session = sessionmaker(bind=engine)
session = scoped_session(Session)

def getNumberOfQuestionsByVideo(videoID):
    questions_n = getQuestionsfromVideo(videoID)
    return len(questions_n)

def getAnswersfromQuestion(questionID):
    question = session.query(Question).filter(Question.id==questionID).first()
    return question.answers

def getAnswersfromQuestionDICT(questionID):
    ret_list = []
    lb = getAnswersfromQuestion(questionID)
    for a in lb:
        ret_list.append(a.to_dictionary())
    return ret_list

def newAnswer(description,qID):
    a = Answer(description = description, question_id = qID)
    try:
        session.add(a)
        session.commit()
        print(a.id)
        session.close()
        return a.id
    except:
        return None

def getQuestionsfromVideo(videoID):
    questions = session.query(Question).filter(Question.video_id==videoID)      #mudei isto, n sei se é suposto ter o first()
    return questions.all()

def getQuestionsfromVideoDICT(videoID):
    ret_list = []
    lb = getQuestionsfromVideo(videoID)
    for b in lb:
        ret_list.append(b.to_dictionary())
    return ret_list

def newQuestion(time , description,vID):
    q = Question(description = description, time = time, video_id = vID)
    try:
        session.add(q)
        session.commit()
        print(q.id)
        session.close()
        return q.id
    except:
        return None


if __name__ == "__main__":
    pass