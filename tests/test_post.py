from app import schema
import pytest

def test_get_all_posts(authorized_client, create_posts):
    res=authorized_client.get("/posts/")
    print("test_get_all_posts.res",res.json())

    def validate(post):
        return schema.PostOut(**post)

    post_map=map(validate, res.json())
    print("list_of_posts",list(post_map))
    res.status_code==200

def test_get_all_post_with_unauthorzed_user(client, create_posts):
    res=client.get("/posts/")
    assert res.status_code==401

def test_get_one_post_with_unauthorzed_user(client, create_posts):
    res=client.get(f"/posts/{create_posts[0].id}")
    assert res.status_code==401

def test_get_one_post_not_exist(authorized_client, create_posts):
    res=authorized_client.get("/posts/9999")
    assert res.status_code==404

def test_get_one_post(authorized_client, create_posts):
    print("test_get_one_post.create_posts",create_posts)
    res=authorized_client.get((f"/posts/{create_posts[0].id}"))
    post=schema.Post(**res.json())
    print("test_get_one_post.res",post)

    assert post.title== create_posts[0].title
    assert post.content== create_posts[0].content
    assert post.id== create_posts[0].id
    assert res.status_code==200


@pytest.mark.parametrize("title, content, is_published",
                        [("title1", "content1", True), ("title2", "content2", False), ("title3", "content3", True)])
def test_create_post(authorized_client, create_posts,create_user, title,content, is_published):
    res = authorized_client.post("/posts/", json={"title": title, "content": content, "is_published": is_published})
    created_post = schema.Post(**res.json())
    print("create_user", create_user.get('id'))
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.is_published == is_published
    assert created_post.owner_id == create_user.get('id')

def test_create_post_default_published(authorized_client, create_user,create_posts):
    res=authorized_client.post("/posts/", json={"title": "title1", "content": "content1"})
    created_post=schema.Post(**res.json())
    assert res.status_code==201
    assert created_post.is_published== True

def test_unauthorized_user_create_post(client, create_posts, create_user):
    res = client.post("/posts/", json={"title": "title1", "content": "content1"})
    assert res.status_code == 401

def test_unauthorized_user_delete_post(client, create_posts, create_user):
    res = client.delete(f"/posts/{create_posts[0].id}")
    assert res.status_code == 401

def test_delete_post_success(authorized_client, create_posts):
    res=authorized_client.delete(f"/posts/{create_posts[0].id}")
    assert res.status_code==204

def test_delete_non_exist_post(authorized_client, create_posts):
    res=authorized_client.delete("/posts/9999")
    assert res.status_code==404

def test_delete_post_not_ow(authorized_client, create_posts):
    res=authorized_client.delete(f"/posts/{create_posts[3].id}")
    assert res.status_code==403

def test_update_post(authorized_client,create_posts):
    data={
        "title": "Today is saturday",
        "content": "I will eat pizza",
        "is_published": True
    }

    res=authorized_client.put(f"/posts/{create_posts[0].id}", json=data)
    updated_post=schema.Post(**res.json())

    assert res.status_code==200
    assert updated_post.title==data.get('title')
    assert updated_post.content==data.get('content')
    assert updated_post.is_published==data.get('is_published')


def test_update_post_not_own(authorized_client, create_posts, create_user2):
    data={
        "title": "Today is saturday",
        "content": "I will eat pizza",
        "is_published": True
    }

    res=authorized_client.put(f"/posts/{create_posts[3].id}", json=data)
    assert res.status_code==403


def test_update_post_unauthozed(client, create_posts):
    data={
        "title": "Today is saturday",
        "content": "I will eat pizza",
        "is_published": True
    }
    res=client.put(f"/posts/{create_posts[0].id}",json=data)
    assert res.status_code==401

def test_update_post_not_exist(authorized_client, create_posts):
    data={
        "title": "Today is saturday",
        "content": "I will eat pizza",
        "is_published": True
    }
    res=authorized_client.put("/posts/9999",json=data)
    assert res.status_code==404