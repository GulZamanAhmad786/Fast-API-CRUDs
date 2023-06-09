from pydantic import BaseModel
from typing import Optional

class Blog(BaseModel):
    title: str
    type: str
    body: str 
    publish: Optional[bool] 


class ShowBlog(BaseModel):
    title: str
    type: str

    class Config:
        orm_mode = True

class User(BaseModel):
    
    name:str
    email:str
    password: str


class ShowUser(BaseModel):
    
    name:str
    email:str
    
    class Config:
        orm_mode = True


class LoginUser(BaseModel):
    
    username:str
    password:str
    
    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None
    

