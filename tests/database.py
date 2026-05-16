from fastapi.testclient import TestClient
from app.main import app

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import setting
from app.model import Base
import pytest
from app.database import get_db

SQLALCHEMY_DATABASE_URL=f"postgresql+psycopg://{setting.database_username}:{setting.database_password}@{setting.database_hostname}:{setting.database_port}/{setting.database_name}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_test_db():
    db = TestSession()

    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db]=get_test_db


@pytest.fixture()
def Session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestSession()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture()
def client(Session):
    def override_get_db():
        try:
            yield Session
        finally:
            Session.close()
    app.dependency_overrides[get_db]=override_get_db
    yield TestClient(app)
