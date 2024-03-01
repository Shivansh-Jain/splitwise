from fastapi import FastAPI
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud, models, schemas
from database import SessionLocal, engine

app  = FastAPI()

models.Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get('/')
def root():
    return {"Hello : World"}

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserBase, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user.user_id)
    if db_user:
        raise HTTPException(status_code=400, detail="User already registered")
    return crud.create_user(db=db, user=user)

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: str, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.post("/create_group/",response_model=schemas.groups)
def create_group(group: schemas.GroupsBase, db :Session = Depends(get_db)):
    db_group = crud.create_group(db = db , group = group)
    return db_group

@app.post('/map_user_group/')
def map_user_group(user_group_mapping: schemas.Users_Groups_Mapping_Base, db : Session = Depends(get_db)):
    map = crud.map_user_group(db=db,user_group_mapping=user_group_mapping)
    return map

@app.get("/get_groups/{user_id}")
def get_groups(user_id: str, db :Session = Depends(get_db)):
    db_group = crud.get_group(db = db,user_id=user_id)
    return db_group

@app.post('/add_transaction')
def add_transaction(transactions : schemas.Transactions , db :Session = Depends(get_db)):
    action = crud.add_transaction(db=db , transactions = transactions)
    return action