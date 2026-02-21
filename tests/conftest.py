import os

import pytest
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.db_config import create_all, drop_all


@pytest.fixture()
def create_connecting():
    db_url = "sqlite:///:memory:"
    engine = create_engine(db_url)
    Session = sessionmaker(bind=engine)
    session = Session()
    create_all(engine)
    yield session
    session.close()
    drop_all(engine)
