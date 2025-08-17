# main.py

from fastapi import FastAPI, status, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

import models # Import our new models file
import schemas
from passlib.context import CryptContext

# --- SQLAlchemy Database Setup ---
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:1973@localhost/ecoeats"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
# This line tells SQLAlchemy to create all our tables based on our models
models.Base.metadata.create_all(bind=engine) 

# --- FastAPI App Setup ---
app = FastAPI()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Dependency to get a database session
def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()

# --- UPDATED USER REGISTRATION ENDPOINT ---
@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse) # Added response_model
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    
    hashed_password = pwd_context.hash(user.password)
    
    new_user_data = user.dict()
    new_user_data.update({"password_hash": hashed_password})
    # Remove the original password, we only want to store the hash
    del new_user_data['password']

    new_user = models.User(**new_user_data)

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return new_user