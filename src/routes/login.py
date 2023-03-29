from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.database import get_db
from src.models import Users
from src.hashing import Hasher
from jose import jwt
from src.config import Config

oauth2_schema = OAuth2PasswordBearer(tokenUrl="login/token")

router = APIRouter()

@router.post('/login/token', tags=["login"])
def retrieve_token_after_authentication(form_data : OAuth2PasswordRequestForm=Depends(), db:Session=Depends(get_db)):
    user = db.query(Users).filter(Users.email==form_data.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Username")
    if not Hasher.verify_hash(form_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = "Invalid Passkey")
    
    data = {"sub" : form_data.username}
    jwt_token = jwt.encode(data, Config.JWT_DICT['ALGORITHM'], Config.JWT_DICT['SECURITY_KEY'])
    return {"acess_token" : jwt_token, "token_type": "bearer"}