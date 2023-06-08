# main.py

from typing import List, Optional

from fastapi import Depends, FastAPI, Response, status, HTTPException
from . import schemas, models , hashing
from sqlalchemy.orm import Session
from blog.database import engine, SessionLocal

from .hashing import Hash


# Clear the existing database tables
#models.Base.metadata.drop_all(bind=engine)

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
items_db = []

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/blog", status_code=status.HTTP_201_CREATED)
async def create(request: schemas.Blog, db: Session= Depends(get_db)):
     new_blog = models.Blog(title=request.title, type=request.type, body= request.body, publish = request.published)
     db.add(new_blog)
     db.commit() 
     db.refresh(new_blog) 
     return new_blog

@app.get('/blogs', response_model= List[schemas.ShowBlog])
async def get_all(db: Session= Depends(get_db)):
    blogs= db.query(models.Blog).all()
    return blogs

@app.get('/blog/{id}', status_code=status.HTTP_200_OK)
async def get_one(id, db: Session= Depends(get_db)):
    blogs= db.query(models.Blog).filter(models.Blog.id==id).first()
    if not blogs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f'BLog not found with id {id}.')
    return blogs

@app.delete('/blog/{id}', status_code= status.HTTP_204_NO_CONTENT)
async def delete_blog(id,  db: Session= Depends(get_db)):
    blog= db.query(models.Blog).filter(models.Blog.id==id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f'BLog not found with id {id}.')
    blog.delete(synchronize_session=False)
    db.commit()
    return 'Deleted'

@app.put('/blog/{id}', status_code= status.HTTP_202_ACCEPTED)
async def update(id, request: schemas.Blog , db: Session= Depends(get_db)):
    blog= db.query(models.Blog).filter(models.Blog.id==id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f'BLog not found with id {id}.')
    blog.update(request.dict())
    db.commit()
    return 'updated'



# Creating Users
@app.post("/user", status_code=status.HTTP_201_CREATED, )
async def create(request: schemas.User, db: Session= Depends(get_db)):
     
     new_blog = models.User(name=request.name, email=request.email, password= Hash.bycrypt(request.password) )
     db.add(new_blog)
     db.commit() 
     db.refresh(new_blog) 
     return new_blog

# Creating Users
@app.delete("/user/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id, db: Session= Depends(get_db)):
    user = db.query(models.User).filter(models.User.id==id)
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f'User not found with id {id}.')
    user.delete(synchronize_session=False)
    db.commit()
    return 'Deleted'




#db.query(models.Blog).filter(models.Blog.id == id).update(request.dict())




