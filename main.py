import colorlog
import logging
import psycopg

from fastapi import FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
import models
from database import engine, get_db

colorlog.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
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

colorlog.info('Create tables')
try:
    models.Base.metadata.create_all(bind=engine)  # Creates the tables in models.py
    print("Tables created successfully.")
except Exception as e:
    print(f"Error creating tables: {e}")

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True  # optional


# Function for other functions to send SQL statements to the database. Uses context
# manager to connect/disconnect every query, don't want to repeat in every function
# param will be an id or a Post object
def execute_query(query_str, query_values=None, query_fetch='one'):
    db_params = {
        "host": "192.168.1.192",
        "port": "5432",
        "user": "rich",
        "password": "reddpos",
        "dbname": "fastapi-course",
    }

    try:
        # Connect to an existing database
        with psycopg.connect(**db_params) as conn:
            colorlog.info(f"conn {conn}")
            # Open a cursor to perform database operations
            with conn.cursor() as cur:
                colorlog.info(f"query_str {query_str}")
                colorlog.info(f"query_values {query_values}")
                cur.execute(query_str, query_values)
                if query_fetch == 'all':
                    data = cur.fetchall()
                elif query_fetch == 'one':
                    data = cur.fetchone()
                    if query_str in ['DELETE', 'INSERT']:
                        conn.commit()

                colorlog.info(f"data {data}")
                colorlog.info(f"type(data) {type(data)}")
                return data  # Execute a command
    except Exception as e:
        colorlog.error(f"Error: {e}")


# my_posts = [{'title': 'title of post 1', 'content': 'content of post 1', 'id': 1},
#             {'title': 'favorite foods', 'content': 'pizza', 'id': 2}]


# def find_post(id):
#     for p in my_posts:
#         if p['id'] == id:
#             return p


# def find_index_post(id):
#     for i, p in enumerate(my_posts, start=1):
#         colorlog.info(f"i: {i}, p: {p}")
#         colorlog.info(f"p['id']: {p['id'] }, id: {id}")
#         if p['id'] == id:
#             return i


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/sqlalchemy")
async def test_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}


# Get one post by id, pydantic type check converts string id to int.
@app.get("/posts/{id}")  # string id
async def get_post(id: int, db: Session = Depends(get_db)):  # string gets converted to int here
    colorlog.info(f"Getting post id {id}")
    # query_str = """SELECT * FROM posts WHERE id = %s"""
    # query_values = (id,)  # tuple items need comma, even if just one
    # post = execute_query(query_str, query_values)

    post =db.query(models.Post).filter(models.Post.id == id).first()  # models.Post has __tablename__

    colorlog.info(f"post {post}")

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} not found.")
    return {"post_detail": post}


# Delete one post, pydantic type check converts string id to int.
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)  # string id
async def delete_post(id: int, db: Session = Depends(get_db)):  # string gets converted to int
    colorlog.info(f"Delete post id {id}")
    # query_str = """DELETE FROM posts WHERE id = %s RETURNING *"""
    # query_values = (id,)  # tuple items need comma, even if just one
    # deleted_post = execute_query(query_str, query_values)

    query = db.query(models.Post).filter(models.Post.id == id)  # models.Post has __tablename__

    if not query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    query.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Get all posts
@app.get("/posts")
async def get_posts(db: Session = Depends(get_db)):
    colorlog.info('Getting all posts')
    # query_str = """SELECT * FROM posts"""
    # posts = execute_query(query_str, query_fetch='all')
    posts = db.query(models.Post).all()
    return {"data": posts}


# # Update a post
@app.put("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_post(id: int, post: Post, db: Session = Depends(get_db)):  # data form front end is in post
    colorlog.info(f"Update post id {id}")
    query_str = """UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *"""
    query_values = (post.title, post.content, post.published, id)

    updated_post = execute_query(query_str, query_values)

    return {"data": updated_post}


# Create a new post, (post: Post) - pydantic verifies passed in is the right type, type Post.
@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(post: Post, db: Session = Depends(get_db)):
    colorlog.info(f"post {post}")
    colorlog.info(f"post.title: {post.title}")
    colorlog.info(f"post.content: {post.content}")
    colorlog.info(f"post.published: {post.published}")

    # query_str = """INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *"""
    # query_values = (post.title, post.content, post.published)
    # new_post = execute_query(query_str, query_values)

    colorlog.info(f"post.model_dump(): {post.model_dump()}")
    new_post = models.Post(**post.model_dump())  # ** is dictionary unpacking, used in function calls
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return {"data": "post created"}
