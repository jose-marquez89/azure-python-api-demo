import logging

from dotenv import load_dotenv
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, relationship 

FORMAT = "%(levelname)s - %(asctime)s - %(message)s"
logging.basicConfig(level=logging.DEBUG, format=FORMAT)

Base = declarative_base()

class Article(Base):
    __tablename__ = 'articles'

    id = Column(Integer, primary_key=True)
    title = Column(String(500))
    abstract = Column(String(1000))
    section_id = Column(ForeignKey("sections.id"))
    author_id = Column(ForeignKey("authors.id"))
    updated_date = Column(DateTime)
    created_date = Column(DateTime)
    published_date = Column(DateTime)
    kicker = Column(String(50))

class Author(Base):
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))

class Section(Base):
    __tablename__ = 'sections'

    id = Column(Integer, primary_key=True)
    name = Column(String(15))

class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String(150))

class ArticleCategory(Base):
    __tablename__ = 'article_category'

    id = Column(Integer, primary_key=True)
    article = Column(ForeignKey('articles.id'))
    category = Column(ForeignKey('categories.id'))

class Url(Base):
    __tablename__ = 'urls'

    article_id = Column(Integer, primary_key=True)
    url = Column(String(500))
    uri = Column(String(500))

class Multimedia(Base):
    __tablename__ = 'multimedia'

    id = Column(Integer, primary_key=True)
    article_id = Column(ForeignKey('articles.id'))
    url = Column(String(500))
    caption = Column(String(500))
    copyright = Column(String(100))

if __name__ == "__main__":
    engine = new_engine()

    Base.metadata.create_all(engine)
