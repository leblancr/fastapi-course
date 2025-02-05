import logging

import colorlog
from fastapi import FastAPI

from .database import engine
from .models import Base
from .routers import post, user, auth

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
    Base.metadata.create_all(bind=engine)  # Creates the tables in models.py
    print("Tables created successfully.")
except Exception as e:
    print(f"Error creating tables: {e}")

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}



