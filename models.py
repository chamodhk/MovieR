from sqlalchemy import Column, Integer, Text, ForeignKey, UniqueConstraint
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, autoincrement= True)
    score = Column(Integer)
    parent_id = Column(Text)
    body = Column(Text)

class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True)
    name = Column(Text, unique=True)


class CommentMovie(Base):
    __tablename__ = "comment_movies"
    comment_id = Column(
        Integer,
        ForeignKey("comments.id"), primary_key=True 
    )
    movie_id = Column(
        Integer,
        ForeignKey("movies.id"), primary_key=True
    )

