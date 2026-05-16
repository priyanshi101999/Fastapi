import pytest
from app import model

@pytest.fixture
def test_vote(Session, create_user, create_posts):
    print("test_vote.create_user",create_user)
    new_vote=model.Vote(post_id=create_posts[3].id,user_id=create_user['id'])
    Session.add(new_vote)
    Session.commit()
    return new_vote



def test_vote_on_post(authorized_client,create_posts):
    res=authorized_client.post("/vote/", json={"post_id": create_posts[3].id, "dir":1})
    assert res.status_code==201

def test_vote_twice(authorized_client, create_posts, test_vote):
    res=authorized_client.post("/vote/", json={"post_id": create_posts[3].id, "dir":1})
    assert res.status_code==409

def test_delete_vote(authorized_client, create_posts, test_vote):
    res=authorized_client.post("/vote/", json={"post_id": create_posts[3].id, "dir":0})
    assert res.status_code==201

def test_delete_vote_not_exist(authorized_client, create_posts):
    res=authorized_client.post("/vote/", json={"post_id": create_posts[3].id, "dir":0})
    assert res.status_code==404

def test_vote_post_not_exist(authorized_client, create_posts):
    res=authorized_client.post("/vote/", json={"post_id": 9999, "dir":1})
    assert res.status_code==404

def test_vote_unauthorized_user(client, create_posts):
    res=client.post("/vote/", json={'post_id':create_posts[3].id, "dir":1})
    assert res.status_code ==401