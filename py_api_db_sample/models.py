import os
import logging
import urllib

import pyodbc
from dotenv import load_dotenv
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship

FORMAT = "%(levelname)s - %(asctime)s - %(message)s"
logging.basicConfig(level=logging.DEBUG, format=FORMAT)

Base = declarative_base()

# TODO: create at least two tables
# Tables will be derived based on the following keys

""" 
    'section', 'subsection', 'title', 'abstract', 'url', 'uri', 
    'byline', 'item_type', 'updated_date', 'created_date', 'published_date', 
    'material_type_facet', 'kicker', 'des_facet', 'org_facet', 
    'per_facet', 'geo_facet', 'multimedia', 'short_url'
"""

# TODO: set foreign ids in the article table 
class Article(Base):
    __tablename__ = 'articles'

    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    abstract = Column(String(200))
    # section_id = Column(ForeignKey(None))
    # url_group_id = Column(ForeignKey(None))
    author_id = Column(ForeignKey("authors.id"))
    updated_date = Column(DateTime)
    created_date = Column(DateTime)
    published_date = Column(DateTime)
    kicker = Column(DateTime)
    # multimedia_id = Column(ForeignKey(None))

# TODO: create the author table
class Author(Base):
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True)
    name = Column(String(20))

# TODO: create the section table
    # this will contain subsection

# TODO: create the category (des_facet) table

# TODO: create the article category table
    # article id
    # category id
    # many-to-one rel to article

if __name__ == "__main__":
    load_dotenv()
    # create a conection
    conn_str_a = "Driver={ODBC Driver 17 for SQL Server};Server=tcp:qbofbi.database.windows.net,1433;Database=python_api_db;Uid=MichaelB;Pwd="
    conn_str_b = "Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
    password = os.environ['DB_PASSWORD'] + ";"
    conn_str_c = conn_str_a + password + conn_str_b
    params = urllib.parse.quote_plus(conn_str_c)
    conn_str = f"mssql+pyodbc:///?odbc_connect={params}"
    engine = create_engine(conn_str, echo=True) 

    logging.debug("Connection OK")
    engine.table_names()