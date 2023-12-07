import logging
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s'
                    )

logging.debug('Debug')
logging.info('info')
logging.warning('warning')
logging.error('error')
logging.critical('critical')

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


@app.get("/")
async def root():
    return {"message": "Hello World"}


# Get one post, pydantic type check converts string id to int.
@app.get("/posts/{id}")  # string id
async def get_post(id: int):  # string gets converted to int
    logging.info(f"Getting post id {id}")
    post = find_post(id)  # int required

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} not found")
    return {"post_detail": post}


# Get all posts
@app.get("/posts")
async def get_posts():
    return {"data": my_posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_posts(post: Post):
    logging.info(f"post {post}")
    logging.info(f"post.title: {post.title}")
    logging.info(f"post.content: {post.content}")
    logging.info(f"post.published: {post.published}")
    logging.info(f"post.rating: {post.rating}")
    logging.info(f"post.dict: {post.model_dump()}")

    post_dict = post.model_dump()
    post_dict['id'] = randrange(0, 1000000)
    my_posts.append(post_dict)

    return {"data": post_dict}
