from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)
from fastapi.security import OAuth2PasswordRequestForm

from Databases.db import get_db
from sqlalchemy.orm import Session
from Models.user import User,UserCreate
from auth import create_access_token
from dependencies import get_current_user

router = APIRouter()

@router.post("/signup")
async def Signup(user: UserCreate,db:Session = Depends(get_db)):
    existing_user = (db.query(User).filter(User.email == user.email).first())
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    else:
        db_user =User(email=user.email,password=user.password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return {"message":"User created successfully"}

@router.post("/login")
async def login(form_data:OAuth2PasswordRequestForm=Depends(),db:Session = Depends(get_db)):
    db_user = (db.query(User).filter(User.email == form_data.username).first())
    if not db_user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    if db_user.password!=form_data.password:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    token = create_access_token(db_user.email)
    return {"access_token":token,"token_type":"bearer"}
@router.get("/profile")
def profile(current_user:User = Depends(get_current_user)):
    return {
        "id":current_user.id,
        "email":current_user.email,
    }
