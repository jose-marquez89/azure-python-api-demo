import logging

from dotenv import load_dotenv
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy import create_engine
import sqlalchemy
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy.sql.expression import true

from pipeline import new_engine, new_session, get_object_id

FORMAT = "%(levelname)s - %(asctime)s - %(message)s"
logging.basicConfig(level=logging.DEBUG, format=FORMAT)

Base = declarative_base()

class Article(Base):
    __tablename__ = 'articles'

    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    abstract = Column(String(200))
    section_id = Column(ForeignKey("sections.id"))
    author_id = Column(ForeignKey("authors.id"))
    updated_date = Column(DateTime)
    created_date = Column(DateTime)
    published_date = Column(DateTime)
    kicker = Column(String(50))

class Author(Base):
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True)
    name = Column(String(20))

class Section(Base):
    __tablename__ = 'sections'

    id = Column(Integer, primary_key=True)
    name = Column(String(15))

class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String(20))

class ArticleCategory(Base):
    __tablename__ = 'article_category'

    article = Column(Integer, primary_key=True)
    category = Column(Integer, primary_key=True)

class Url(Base):
    __tablename__ = 'urls'

    article_id = Column(Integer, primary_key=True)
    url = Column(String(500))
    uri = Column(String(500))

class Multimedia(Base):
    __tablename__ = 'multimedia'

    article_id = Column(Integer, primary_key=True)
    url = Column(String(500))
    caption = Column(String(500))
    copyright = Column(String(30))

if __name__ == "__main__":
    load_dotenv()

    engine = new_engine()
    session = new_session(engine)

    new_artcat = ArticleCategory(article=34, category=56)
    session.add(new_artcat)
    session.commit()
    session.close()
