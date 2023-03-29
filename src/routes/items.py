from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from src.schemas import  ShowItem, CreateItem
from src.models import Items, applyMigrations, Users
from src.database import get_db
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List
from src.routes.login import oauth2_schema
from jose import jwt
from src.config import Config

router = APIRouter()

applyMigrations()

def get_user_from_token(db, token):
    try:
        payload = jwt.decode(token, Config.JWT_DICT['ALGORITHM'], Config.JWT_DICT['SECURITY_KEY'])
        username = payload.get("sub")
        if not username:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate Credentials",
            )
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate Credetials",
        )
    user = db.query(Users).filter(Users.email == username).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
    return user

@router.get('/items/all', tags = ['items'], response_model=List[ShowItem])
def retrieve_all(db:Session = Depends(get_db)):
    items = db.query(Items).all()
    if not items:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No Items Found.")
    return items
 
@router.get('/items/{id}', tags = ['items'], response_model=ShowItem)
def retrieve_item_by_id(id:int, db:Session = Depends(get_db)):
    item = db.query(Items).filter(Items.id == id).first()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Item {id} does not exist.")
    return item

@router.post('/items/', tags=['items'], response_model=ShowItem)
def create_item(item: CreateItem, db:Session = Depends(get_db), token:str = Depends(oauth2_schema)):
    user = get_user_from_token(db, token)
    owner_id = user.id
    item = Items(**item.dict(), date_posted=datetime.now().date(), owner_id=owner_id)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
        
@router.put("/items/update/{id}", tags=['items'])
def update_by_id(id:int, item : CreateItem, db:Session = Depends(get_db), token:str = Depends(oauth2_schema)):
    user = get_user_from_token(db, token)

    item_exist = db.query(Items).filter(Items.id == id)
    if not item_exist.first():
        return {"message": f"No Details found for Item ID {id}"}
    if item_exist.first().owner_id == user.id:
        item_exist.update(jsonable_encoder(item))
        db.commit()
        return {"message": f"Details successfully updated for Item ID {id}"}
    else:
        return {"message": "You are not authorized"}

@router.delete("/item/delete/{id}", tags=['items'])
def delete_by_id(id:int,db:Session = Depends(get_db), token:str = Depends(oauth2_schema)):
    user = get_user_from_token(db, token)
    item_exist = db.query(Items).filter(Items.id==id)
    if not item_exist.first():
        return {"message": f"No Details found for Item ID {id}"}
    if item_exist.first().owner_id == user.id:
        item_exist.delete()
        db.commit()
        return {"message": f"Item ID {id} has been successfully deleted"}
    else:
        return {"message": "You are not authorized"}
