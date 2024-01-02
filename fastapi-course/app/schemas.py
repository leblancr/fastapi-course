from datetime import datetime

from pydantic import BaseModel, EmailStr


# Pydantic models for validation of data received from requests and sent back in response
# Requests
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True  # optional


class PostCreate(PostBase):
    pass


# Response
class Post(PostBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True  # converts sqlalchemy model returned to pydantic model (dictionary)


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True  # converts sqlalchemy model returned to pydantic model (dictionary)


