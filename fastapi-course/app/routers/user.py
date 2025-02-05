import colorlog
from typing import List

from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from .. import schemas, models, utils
from .. database import get_db

router = APIRouter(
    prefix='/users',  # url path starts with this
    tags=['users']
)


# Create a new user, (user: schemas.UserCreate) - pydantic verifies passed in is this type
@router.post("", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    colorlog.info(f"user.model_dump(): {user.model_dump()}")

    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.model_dump())  # ** is dictionary unpacking, used in function calls
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# Get one user by id, pydantic type check converts string id to int.
@router.get("/{id}", response_model=schemas.UserOut)  # string id
async def get_user(id: int, db: Session = Depends(get_db)):  # string gets converted to int here
    colorlog.info(f"Getting user id {id}")
    user = db.query(models.User).filter(models.User.id == id).first()  # models.User has __tablename__
    colorlog.info(f"user {user}")

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id {id} not found.")
    return user
