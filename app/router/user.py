from .. import model, schema, util , oauth2 
from fastapi import Depends, status, APIRouter
from ..database import get_db
from sqlalchemy.orm import Session

router= APIRouter(prefix='/users', tags=['users'])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.UserOut)
def userCreate(user:schema.UserCreate, db : Session = Depends(get_db)):
    try:
        hashed_password = util.hash(user.password)
        user.password = hashed_password
        new_user = model.User(**user.model_dump())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    except Exception as error:
        print("Error:", error)  
        return { "error": str(error) or error}

@router.get("/{id}", response_model = schema.UserOut)
def get_user(id: int, db : Session = Depends(get_db), user_id : int = Depends(oauth2.get_current_user)):

    user = db.query(model.User).filter(model.User.id == id).first()

    if user is None:
        raise Exception(status_code=status.HTTP_404_NOT_FOUND, detail=f"user not found with id: {id}")
    
    return user
