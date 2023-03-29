from pydantic import EmailStr, BaseModel
from datetime import date

class CreateUser(BaseModel):
    email : EmailStr
    password : str

class ShowUser(BaseModel):              
    email : EmailStr
    is_active : bool
    # It return orm mapper or class object not dictionary. To do so we are using config class.
    class Config:
        orm_mode = True

class CreateItem(BaseModel):
    title : str
    description : str

class ShowItem(BaseModel):
    title : str
    description : str
    date_posted : date
    # It return orm mapper or class object not dictionary. To do so we are using config class.
    class Config:
        orm_mode = True