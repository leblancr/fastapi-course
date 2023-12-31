from pydantic import BaseModel


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True  # optional


class PostCreate(PostBase):
    pass


