from fastapi import  APIRouter, Depends
from sqlalchemy.orm import Session
from .. import models, schemas, database , token
from fastapi import HTTPException,status
from .. hashing import Hash
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter(tags=['Auth'])
get_db = database.get_db


@router.post('/login')
async def login_user(request: OAuth2PasswordRequestForm = Depends(),  db: Session = (Depends(get_db))):
    login_user = db.query(models.User).filter(models.User.email == request.username).first()
    if not login_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Invalid Credentails!')
    if not Hash.verify(request.password, login_user.password):
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Incorrect Password!')
    access_token = token.create_access_token(data={"sub": login_user.email})
    return {"access_token": access_token, "token_type": "bearer"}
    