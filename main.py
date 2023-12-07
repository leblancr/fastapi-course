import logging
from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel

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


my_posts = {}


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/createposts")
async def create_posts(post: Post):
    logging.info(f"post {post}")
    logging.info(f"post.title: {post.title}")
    logging.info(f"post.content: {post.content}")
    logging.info(f"post.published: {post.published}")
    logging.info(f"post.rating: {post.rating}")
    logging.info(f"post.dict: {post.dict()}")
    
    return {"data": post}
