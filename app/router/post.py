from .. import model, schema, util, oauth2
from fastapi import Depends,HTTPException, status, APIRouter, Response
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import func

router=APIRouter(prefix='/posts', tags=['Posts'])

@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schema.PostOut])
def get_posts(db : Session= Depends(get_db), current_user=Depends(oauth2.get_current_user),limit:int=3,skip:int=0, search:Optional[str]=""):
    # cursor.execute('SELECT * FROM public."Posts"')
    # posts = cursor.fetchall()

    posts = db.query(model.Post).filter(model.Post.title.contains(search)).limit(limit).offset(skip).all()

    result = db.query(model.Post, func.count(model.Vote.post_id).label("votes")).join(model.Vote,model.Post.id==model.Vote.post_id, isouter=True).group_by(model.Post.id).filter(model.Post.title.contains(search)).limit(limit).offset(skip).all()

    postList = []
    for post, vote in result:
        print("POST:", post.id, post.title, post.owner)
        print("VOTE:", vote)

        postList.append({"post":{"id":post.id, "title":post.title, "content":post.content, "is_published":post.is_published, "owner":post.owner, "created_at":post.created_at, "owner_id":post.owner_id},"vote":vote})

    return postList

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.Post)
def new_post(post: schema.PostCreate, db : Session = Depends(get_db), current_user =Depends(oauth2.get_current_user) ):
    try:
        # cursor.execute('INSERT INTO public."Posts" (title,content, is_published) VALUES ( %s, %s, %s) RETURNING *', (post.title, post.content, post.is_published))
        # new_post = cursor.fetchone()
        # connect.commit()
        # return {"new_Post":new_post}
        print(post.model_dump())

        new_post = model.Post(**post.model_dump(), owner_id=current_user.id)
        db.add(new_post)
        db.commit()
        db.refresh(new_post)

        return new_post

    except Exception as error:
        print("Error: ", error)
        return {"Error": "Failed to add post"}


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schema.Post)
def get_post(id: int, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    print("id:",type(id))
    # cursor.execute('SELECT * FROM public."Posts" WHERE id=%s', (id,))
    # post = cursor.fetchone()
    post = db.query(model.Post).filter(model.Post.id == id).first()
    print(post)
       
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} not found")
    return post


   

@router.delete("/{id}")
def deletePost(id : int, db : Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):

    # cursor.execute('DELETE FROM public."Posts" WHERE id= %s RETURNING*', (id,))
    # deleted_post=cursor.fetchone()
    # connect.commit()

    post_query = db.query(model.Post).filter(model.Post.id ==id)

    post = post_query.first()

    if post is None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"The post with id = {id} not found")
    print("deleted post", post)

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
        
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)






@router.put("/{id}", response_model=schema.Post)
def updatePost(id: int, update_post : schema.PostCreate, db : Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):

        # cursor.execute('UPDATE public."Posts" SET title = %s, content= %s, is_published = %s WHERE id= %s RETURNING *', (post.title, post.content, post.is_published, id))
        # updated_post = cursor.fetchone()

        # connect.commit()


    post_query=db.query(model.Post).filter(model.Post.id == id)

    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail =f"post with id: {id} not found")
        
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorized to perform requested action")
       
    post_query.update(update_post.model_dump(), synchronize_session=False)
    db.commit()

    return post_query.first()
    

    

