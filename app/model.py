from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship

class Post(Base):
    __tablename__ = "Posts"

    id = Column(Integer, primary_key=True, nullable=False, index=True)
    title = Column(String,  nullable=False)
    content=Column(String, nullable=False)
    is_published=Column(Boolean, nullable=False, server_default='TRUE')
    created_at=Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    owner = relationship("User")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, nullable=False, primary_key=True, index=True)
    email = Column(String, nullable=True, unique=True )
    password=Column(String, nullable=False)
    created_at=Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    phone=Column(Integer, nullable=True)



class Vote(Base):
    __tablename__="vote"

    post_id=Column(Integer, ForeignKey("Posts.id", ondelete="CASCADE"), primary_key=True, nullable=False)
    user_id=Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True, nullable=False)
