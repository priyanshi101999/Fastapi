from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, Literal


class PostBase(BaseModel):
    title: str
    content: str
    is_published: bool = True

class PostCreate(PostBase):
    pass

class UserOut(BaseModel):
    email: EmailStr
    created_at: datetime
    id: int


class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut
    class Config:
        orm_mode = True

class PostOut(BaseModel):
    post: Post
    vote: int

    class Config:
        orm_mode=True

class UserCreate(BaseModel):
    email: EmailStr
    password: str



class user_Credentials(BaseModel):
    email : EmailStr
    password: str

class Token(BaseModel):
    token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None


class VoteData(BaseModel):
    post_id: int
    dir: Literal[0,1]