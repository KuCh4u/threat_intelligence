from sqlalchemy import Column, Integer, String, Text, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class Feed(Base):
    __tablename__ = 'feeds'
    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False)
    url = Column(Text, nullable=False)

class Keyword(Base):
    __tablename__ = 'keywords'
    id = Column(Integer, primary_key=True)
    word = Column(String(64), nullable=False)

class Article(Base):
    __tablename__ = 'articles'
    id = Column(Integer, primary_key=True)
    title = Column(Text)
    summary = Column(Text)
    link = Column(Text, unique=True)
    source = Column(String(128))
