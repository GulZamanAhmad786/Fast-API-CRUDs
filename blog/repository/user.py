
from sqlalchemy.orm import Session
from .. import models, schemas
from fastapi import HTTPException,status
from ..hashing import Hash
from .. repository import user

def create(request: schemas.User, db: Session):
    new_user = models.User(name=request.name, email=request.email, password= Hash.bycrypt(request.password) )
    db.add(new_user)
    db.commit() 
    db.refresh(new_user )
    return new_user


def show_all(db: Session):
    users = db.query(models.User).all()
    return users
   
   
def get_one(id:int,db:Session):
    user = db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f'User not found with id {id}.')
    return user

def destroy(id:int,db: Session):
    user = db.query(models.User).filter(models.User.id==id)
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f'User not found with id {id}.')
    user.delete(synchronize_session=False)
    db.commit()
    return 'Deleted'