import requests
import os
import logging
import urllib
from dotenv import load_dotenv

from sqlalchemy import create_engine, exc 
from sqlalchemy.orm import sessionmaker

FORMAT = "%(levelname)s - %(asctime)s - %(message)s"
logging.basicConfig(level=logging.DEBUG, format=FORMAT)

# TODO: Morph below into a reuable class or function for use within
# the Azure function

load_dotenv()

def get_data(section='science'):
    base_url = "https://api.nytimes.com/svc/topstories/v2/science.json"
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
    print("Data Size:", len(ny_data))
    print("Keys: ", ny_data.keys())

    results = ny_data["results"]
    print("Results size: ", len(results))

    result_zero = results[0]
    print("First Result Keys: ", result_zero.keys())

    for key, value in result_zero.items():
        print(key, end=": ")
        print(value)

    rkeys = result_zero.keys()
    same_keys = []
    item_type = []

    for result in results:
        same_keys.append(result.keys() == rkeys)
        item_type.append(result['item_type'])

    logging.debug(all(same_keys))
    logging.debug(all(map(lambda x: x == 'Article', item_type)))

    url_lengths = []
    for item in result_zero['multimedia']:
        url_lengths.append(len(item['url']))

    print("Average length", sum(url_lengths)/ len(url_lengths))
