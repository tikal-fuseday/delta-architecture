from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, \
     ForeignKey, event
from sqlalchemy.orm import scoped_session, sessionmaker, backref, relation
from sqlalchemy.ext.declarative import declarative_base

from werkzeug import cached_property, http_date

from flask import url_for, Markup

engine = create_engine('postgres://localhost/fake',
                       convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

def init_db():
    Base.metadata.create_all(bind=engine)


Base = declarative_base()
Base.query = db_session.query_property()


class Voter(Base):
    __tablename__ = 'voters'
    id = Column(String(9), primary_key=True)
    name = Column(String(50))
    address = Column(String(50))
    gender = Column(String(50))
    race = Column(String(50))
    bibist = Column(String(1))


class Poll(Base):
    __tablename__ = 'polls'
    id = Column('id', Integer, primary_key=True)
    voter_id = Column(String(9), ForeignKey('voters.id'))
    answer = Column(String(50))
    created_at = Column(DateTime(), default=datetime.now)
