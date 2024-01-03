import logging

import colorlog
from typing import List

from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from .. import schemas, models
from .. database import get_db

router = APIRouter(
    prefix='/posts',  # url path starts with this
    tags=['posts']
)


# Get one post by id, pydantic type check converts string id to int.
@router.get("/{id}", response_model=schemas.Post)  # string id
async def get_post(id: int, db: Session = Depends(get_db)):  # string gets converted to int here
    colorlog.info(f"Getting post id {id}")
    post =db.query(models.Post).filter(models.Post.id == id).first()  # models.Post has __tablename__

    colorlog.info(f"post {post}")

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} not found.")
    return post


# Delete one post, pydantic type check converts string id to int.
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)  # string id
async def delete_post(id: int, db: Session = Depends(get_db)):  # string gets converted to int
    colorlog.info(f"Delete post id {id}")
    query = db.query(models.Post).filter(models.Post.id == id)  # models.Post has __tablename__

    if not query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Get all posts
@router.get("", response_model=List[schemas.Post])
async def get_posts(db: Session = Depends(get_db)):
    colorlog.info('Getting all posts')
    posts = db.query(models.Post).all()  # models.Post is __tablename__

    return posts


# Update a post
@router.put("/{id}", response_model=schemas.Post)
async def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):  # data form front end is in post
    colorlog.info(f"Update post id {id}")
    query = db.query(models.Post).filter(models.Post.id == id)  # models.Post is __tablename__

    if not query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    query.update(post.model_dump())
    db.commit()

    return {"data": query.first()}


# Create a new post, (post: schemas.PostCreate) - pydantic verifies passed in is this type
@router.post("", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
async def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    colorlog.info(f"post.model_dump(): {post.model_dump()}")
    new_post = models.Post(**post.model_dump())  # ** is dictionary unpacking, used in function calls
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post
