from fastapi import (
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from Databases.db import get_db

from Models.user import User

from auth import verify_token
from security import oauth2_scheme

def get_current_user(token: str = Depends(oauth2_scheme),db: Session = Depends(get_db)):
    email=verify_token(token)
    if not email:
        raise HTTPException(status_code=400,detail="Incorrect email or password")
    user = db.query(User).filter(User.email==email).first()
    if not user:
        raise HTTPException(status_code=400,detail="User not Found")
    return user