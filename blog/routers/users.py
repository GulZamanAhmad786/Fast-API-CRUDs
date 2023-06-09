from typing import List
from fastapi import Depends,  status, APIRouter
from .. import schemas,  database
from sqlalchemy.orm import Session
from blog.database import engine, SessionLocal
from .. hashing import Hash
from .. repository import user



router= APIRouter(
    tags=['users'],
    prefix='/user'
)
get_db = database.get_db


# Creating Users
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(request: schemas.User, db: Session= Depends(get_db)):
     return user.create(request,db)


@router.get("/{id}",  status_code=status.HTTP_200_OK, )
async def get_user(id:int, db: Session= Depends(get_db)):
    return user.get_one(id,db)

@router.get('/', status_code=status.HTTP_200_OK, response_model=List[schemas.ShowUser])
async def get_all_user(db: Session= Depends(get_db)):
    return user.show_all(db)



@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id, db: Session= Depends(get_db)):
    user.destroy(id,db)