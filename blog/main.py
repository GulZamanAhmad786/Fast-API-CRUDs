# main.py

from . import  models ,  database  
from blog.database import engine
from .routers import blogs , users , auth
from fastapi import FastAPI


# Clear the existing database tables
#models.Base.metadata.drop_all(bind=engine)

models.Base.metadata.create_all(bind=engine)
 
app = FastAPI()

app.include_router(auth.router)
app.include_router(blogs.router)
app.include_router(users.router)








