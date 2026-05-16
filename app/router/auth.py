from fastapi import APIRouter, HTTPException, status,Depends, Form
from .. import model, oauth2, schema, util
from sqlalchemy.orm import Session
from ..database import get_db
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter(tags = ["Authentication"])

@router.post("/login", response_model=schema.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db : Session = Depends(get_db)):
    user = db.query(model.User).filter(model.User.email == user_credentials.username).first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User not found")
        
    if not util.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"invalid credentials")
        

    access_token = oauth2.create_jwt_token(data = {"user_id": user.id})
    return {"token": access_token, "token_type": "bearer"}
    



