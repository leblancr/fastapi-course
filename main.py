import colorlog
import logging

from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange

colorlog.basicConfig(level=logging.DEBUG,
                     format='%(asctime)s - %(levelname)s - %(message)s'
                     )
colorlog.debug("debug")
colorlog.info("info")
colorlog.warning("warning")
colorlog.error("error")
colorlog.critical("critical")

# logging.basicConfig(level=logging.DEBUG,
#                     format='%(asctime)s - %(levelname)s - %(message)s'
#                     )

# logging.debug('Debug')
# logging.info('info')
# logging.warning('warning')
# logging.error('error')
# logging.critical('critical')

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True  # optional
    rating: Optional[int] = None


my_posts = [{'title': 'title of post 1', 'content': 'content of post 1', 'id': 1},
            {'title': 'fovorite foods', 'content': 'pizza', 'id': 2}]


def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p


def find_index_post(id):
    for i, p in enumerate(my_posts, start=1):
        colorlog.info(f"i: {i}, p: {p}")
        colorlog.info(f"p['id']: {p['id'] }, id: {id}")
        if p['id'] == id:
            return i


@app.get("/")
async def root():
    return {"message": "Hello World"}


# Get one post, pydantic type check converts string id to int.
@app.get("/posts/{id}")  # string id
async def get_post(id: int):  # string gets converted to int
    colorlog.info(f"Getting post id {id}")
    post = find_post(id)  # int required

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} not found")
    return {"post_detail": post}


# Delete one post, pydantic type check converts string id to int.
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)  # string id
async def delete_post(id: int):  # string gets converted to int
    colorlog.info(f"Delete post id {id}")
    index = find_index_post(id)  # int required
    colorlog.info(f"index {index}")

    if not index:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    my_posts.pop(index - 1)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Get all posts
@app.get("/posts")
async def get_posts():
    return {"data": my_posts}


# Update a post
@app.put("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_post(id: int, post: Post):  # data form front end is in post
    colorlog.info(f"Update post id {id}")
    index = find_index_post(id)  # int required

    if not index:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    post_dict = post.model_dump()
    post_dict['id'] = id
    my_posts[index] = post_dict  # replace with new post

    return {"data": post_dict}


# Create a new post
@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_posts(post: Post):
    colorlog.info(f"post {post}")
    colorlog.info(f"post.title: {post.title}")
    colorlog.info(f"post.content: {post.content}")
    colorlog.info(f"post.published: {post.published}")
    colorlog.info(f"post.rating: {post.rating}")
    colorlog.info(f"post.dict: {post.model_dump()}")

    post_dict = post.model_dump()
    post_dict['id'] = randrange(0, 1000000)
    my_posts.append(post_dict)

    return {"data": post_dict}
