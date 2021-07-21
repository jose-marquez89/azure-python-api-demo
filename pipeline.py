from datetime import time
import requests
import os
import logging
import urllib
import re
from datetime import datetime as dt
from dotenv import load_dotenv

from sqlalchemy import create_engine, exc 
from sqlalchemy.orm import sessionmaker
from models import Article, Author, Section, Category, ArticleCategory, Url, Multimedia

FORMAT = "%(levelname)s - %(asctime)s - %(message)s"
logging.basicConfig(level=logging.DEBUG, format=FORMAT)

load_dotenv()

def get_data(section='science'):
    base_url = "https://api.nytimes.com/svc/topstories/v2"
    url_cat = f"/{section}.json" 
    api_key = os.environ["NYT_KEY"]
    key_param = f"?api-key={api_key}"
    res = requests.get(base_url + key_param)
    
    try:
        res.raise_for_status()
    except Exception as err:
        logging.error(err)
        return

    data = res.json()

    return data

def new_session(engine):
    Session = sessionmaker()
    Session.configure(bind=engine)

    return Session()

def get_object_id(object_name, table, session):
    try:
        object = session.query(table)
        object = object.filter(table.name == object_name).one()
        
        return object.id
    except exc.NoResultFound:
        new_object = table(name=object_name)
        session.add(new_object)
        session.commit()

        object = session.query(table)
        object = object.filter(table.name == object_name).one()

        return object.id

def insert_story(result, session):
    author_ptn = r'(\w+\s)(.*)'
    timeformat = "%Y-%m-%dT%X"

    # necessary ids
    section_id = get_object_id(result['section'], Section, session)
    author_name = re.search(author_ptn, result['byline']).group(2) 
    author_id = get_object_id(author_name, Author, session)

    # article data
    title = result['title']
    abstract = result['abstract']
    url = result['url']
    uri = result['uri']
    updated_date = dt.strptime(result['updated_date'][:-6], timeformat)
    created_date = dt.strptime(result['created_date'][:-6], timeformat)
    published_date = dt.strptime(result['published_date'][:-6], timeformat)
    kicker = result['kicker']

    new_article = Article(title=title, abstract=abstract, section_id=section_id,
                          author_id=author_id, updated_date=updated_date, created_date=created_date,
                          published_date=published_date, kicker=kicker) 

    session.add(new_article)
    session.commit()

    # url table data
    url = result['url']
    uri = result['uri']

    article_urls = Url(url=url, uri=uri, article_id=new_article.id)
    session.add(article_urls)
    session.commit()

    # lists
    categories = result['des_facet']
    multimedia = result['multimedia']

    category_entries = []
    for category in categories:
        catid = get_object_id(category, Category, session)
        category_relation = ArticleCategory(article=new_article.id, category=catid)
        category_entries.append(category_relation)

    session.add_all(category_entries)
    session.commit()

    media_entries = []
    for media in multimedia:
        new_media = Multimedia(article_id=new_article.id, url=media['url'], 
                               caption=media['caption'], copyright=media['copyright'])
        media_entries.append(new_media)
    
    session.add_all(media_entries)
    session.commit()

def new_engine():
    password = os.environ['DB_PASSWORD']
    server_name = os.environ['DB_SERVER']
    db_name = os.environ['DB_NAME']
    uid = os.environ['DB_USER']

    driver = "Driver={ODBC Driver 17 for SQL Server};"
    connections = f"Server=tcp:{server_name}.database.windows.net,1433;Database={db_name};Uid={uid};Pwd={password};"
    params = "Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
    azure_conn_raw = driver + connections + params 
    azure_conn = urllib.parse.quote_plus(azure_conn_raw)
    conn_str = f"mssql+pyodbc:///?odbc_connect={azure_conn}"
    engine = create_engine(conn_str, echo=True) 

    return engine


if __name__ == "__main__":
    ny_data = get_data()
    results = ny_data["results"]
    result_zero = results[0]

    engine = new_engine()
    session = new_session(engine)

    insert_story(result_zero, session)
