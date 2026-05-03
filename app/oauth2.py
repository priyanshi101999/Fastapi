import jwt 
from jwt.exceptions import PyJWTError
from datetime import datetime, timedelta, timezone
from . import schema, database, model
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from .config import setting

oauth_scheme = OAuth2PasswordBearer("login")

SECRET_KEY = setting.secret_key
ALGORITHM = setting.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = setting.access_token_expire_minutes


def create_jwt_token(data: dict):
    encoded = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    encoded.update({"exp": expire})

    return jwt.encode(encoded, SECRET_KEY, algorithm=ALGORITHM)

def verify_jwt_token(token: str, credencials_exception):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        id = payload.get("user_id")

        if id is None:
            raise credencials_exception
    
        token_data=schema.TokenData(id=id)
        if token_data is None:
            raise credencials_exception
        
    except PyJWTError:
        raise credencials_exception
    
    return token_data


def get_current_user(token: str = Depends(oauth_scheme), db : Session = Depends(database.get_db)):
    credencials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="could not validate credencials",
        headers={"WWW-AUTHENTICATE":"Bearer"}
    )

    token_data =  verify_jwt_token(token, credencials_exception)

    user = db.query(model.User).filter(model.User.id == token_data.id).first()

    return user

   
    