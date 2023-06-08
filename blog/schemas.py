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