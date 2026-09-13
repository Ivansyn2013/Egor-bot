from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import pytest
import os
from models.db_config import create_all, drop_all

@pytest.fixture()
def create_connecting():
    load_dotenv(dotenv_path='../.env_test')  # тут подумать как пробрасывать все настройки из мейн

    username = os.getenv("MYSQL_USER")
    password = os.getenv("MYSQL_PASSWORD")
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    database_name = os.getenv("MYSQL_DATABASE")

    db_url = f'mysql+mysqlconnector://{username}:{password}@{host}:{port}/{database_name}'
    engine = create_engine(db_url)
    Session = sessionmaker(bind=engine)
    session = Session()
    create_all(engine)
    yield session
    session.close()
    drop_all(engine)

