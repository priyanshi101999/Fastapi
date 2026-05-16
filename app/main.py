from typing import List
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg
import time
from .database import engine
from . import model
from .router import user, post, auth, vote
from fastapi.middleware.cors import CORSMiddleware


# model.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
@app.get("/")
def test():
    return {"message": "Hello World!!"}

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)
 