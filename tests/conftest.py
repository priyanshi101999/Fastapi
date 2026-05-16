from fastapi.testclient import TestClient
from app.main import app
from app.oauth2 import create_jwt_token
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import setting
from app.model import Base
import pytest
from app.database import get_db
from app import model

SQLALCHEMY_DATABASE_URL=f"postgresql+psycopg://{setting.database_username}:{setting.database_password}@{setting.database_hostname}:{setting.database_port}/{setting.database_name}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)

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

@pytest.fixture
def create_user(client):
    user_data={"email":"maya@gmail.com", "password":"1234"}
    res = client.post("/users/", json=user_data)
    new_user=res.json()
    new_user["password"]=user_data["password"]
    print("create_user.res",new_user)
    assert res.status_code==201
    return new_user

@pytest.fixture
def create_user2(client):
    user_data={"email":"sara@gmail.com", "password":"1234"}
    res = client.post("/users/", json=user_data)
    new_user=res.json()
    new_user["password"]=user_data["password"]
    print("create_user.res",new_user)
    assert res.status_code==201
    return new_user


@pytest.fixture
def get_token(create_user):
    token=create_jwt_token(data={"user_id":create_user["id"]})
    return token

@pytest.fixture
def authorized_client(client, get_token):
    client.headers={
        **client.headers,
        "Authorization":f"Bearer {get_token}"
    }
    return client


@pytest.fixture
def create_posts(create_user,create_user2, Session):
    post_Data=[{
        "title":"post 1",
        "content":"It's beach day",
        "owner_id":create_user['id']
    },
    {
        "title":"post 2",
        "content":"It's sun day",
        "owner_id":create_user['id']
    },
    {
        "title":"post 3",
        "content":"It's fun day",
        "owner_id":create_user['id']
    },
    {
        "title":"post 4",
        "content":"It's party day",
        "owner_id":create_user2['id']
    }
    ]

    def map_post(post):
        print("single_post", post)
        return model.Post(**post)
    
    post_map =map(map_post, post_Data)
    print("mapped_post",post_map)
    posts = list(post_map)
    print("posts_list",posts)

    Session.add_all(posts)
    Session.commit()
    created_posts=Session.query(model.Post).all()
    return created_posts
