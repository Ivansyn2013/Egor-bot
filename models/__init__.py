import logging

from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import  sessionmaker
from .subscribers import *
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path='.env_test')#тут подумать как пробрасывать все настройки из мейн

username = os.getenv("MYSQL_USER")
password = os.getenv("MYSQL_PASSWORD")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
database_name = os.getenv("MYSQL_DATABASE")

db_url = f'mysql+mysqlconnector://{username}:{password}@{host}:{port}/{database_name}'
print(db_url)

engine = create_engine(db_url, echo=True)

inspector = inspect(engine)
table_names = inspector.get_table_names()
table_tuple  = (Subscriber.__tablename__, UserRequest.__tablename__)
if any(map(lambda x: x not in table_names, table_tuple)):
    logging.debug('Tables not found in database and try to create')
    Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
db = Session()
