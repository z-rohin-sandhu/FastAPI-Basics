from fastapi import APIRouter, Depends,HTTPException, status
from src.schemas import CreateUser, ShowUser
from src.models import Users, applyMigrations
from src.hashing import Hasher
from src.database import get_db
from sqlalchemy.orm import Session
from typing import List

router = APIRouter()

applyMigrations()

@router.get('/users/all', tags = ['users'], response_model=List[ShowUser])
def retrieve_all(db:Session = Depends(get_db)):
    users = db.query(Users).all()
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No Users Found.")
    return users

@router.get('/users/{id}', tags = ['users'], response_model=ShowUser)
def retrieve_User_by_id(id:int, db:Session = Depends(get_db)):
    user = db.query(Users).filter(Users.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User {id} does not exist.")
    return user

@router.post('/users/', tags=['users'], response_model=ShowUser)
def create_user(user: CreateUser, db:Session = Depends(get_db)):
    user = Users(email=user.email, password=Hasher.get_hash(user.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user