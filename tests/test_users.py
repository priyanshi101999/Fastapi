from app import schema
import pytest
from app.config import setting
import jwt

def test_root(client):
    res=client.get("/")
    assert res.json().get('message')=='Hello World'
    assert res.status_code==200


def test_create_user(client):
    res=client.post("/users/", json={'email': "el@gmail.com", "password":"1234" })
    new_user=schema.UserOut(**res.json())
    assert new_user.email=="el@gmail.com"
    assert res.status_code==201




def test_login(create_user, client):
    res=client.post("/login", data={"username": create_user["email"], "password":create_user["password"]})
    print("test_login.res",res.json())
    login_res = res.json()
    payload = jwt.decode(login_res['token'], setting.secret_key, algorithms=[setting.algorithm])
    print("test_login.payload",payload)
    assert payload['user_id']==create_user['id']
    assert login_res.get('token_type')=='bearer'
    assert res.status_code==200


@pytest.mark.parametrize("email, password, status_code",[
    ("maya@gmail.com", "wrongPassword", 403),
    # ("maya@yop.com", "123456", 404),
    (None, "1234", 422),
    ("maya@gmail.com", None, 422)

])
def test_invalid_login(create_user, client, email, password, status_code):
    print("test_invalid_login.create_user",create_user, email, password, status_code)
    res=client.post("/login", data={"username": email, "password":password})
    assert res.status_code==status_code
    


