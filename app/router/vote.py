from fastapi import APIRouter, status, Depends, HTTPException
from .. import schema, model, oauth2, database
from sqlalchemy.orm import Session

router=APIRouter(prefix="/vote", tags=['Vote'])

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote:schema.VoteData, db : Session = Depends(database.get_db), current_user= Depends(oauth2.get_current_user)):

    vote_query = db.query(model.Vote).filter(model.Vote.post_id==vote.post_id, model.Vote.user_id==current_user.id)
    post = db.query(model.Post).filter(model.Post.id==vote.post_id).first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {vote.post_id} not found")
    found_vote=vote_query.first()

    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"post with id {vote.post_id} is already voted")
        
        new_vote=model.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "Vote is added successfully"}
        
        
    else:
        if found_vote:
            vote_query.delete()
            db.commit()
            return {"message": "Vote is deleted successfully"}
        
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {vote.post_id} is not voted")
       