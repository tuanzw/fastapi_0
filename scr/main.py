from fastapi import FastAPI, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session

import services as _services, schemas as _schemas

app = FastAPI()

_services.create_database()


@app.get("/users/", response_model=List[_schemas.User])
def get_users(skip: int = 0, limit: int = 10, db: Session = Depends(_services.get_db)):
    return _services.get_users(skip=skip, limit=limit, db=db)


@app.get("/users/{user_id}", response_model=_schemas.User)
def get_user(user_id: int, db: Session = Depends(_services.get_db)):
    db_user = _services.get_user(user_id=user_id, db=db)
    if db_user is None:
        raise HTTPException(
            status_code=404, detail=f"user with id ({user_id}) does not exist"
        )
    return db_user


@app.post("/users/", response_model=_schemas.User)
def create_user(user: _schemas.UserCreate, db: Session = Depends(_services.get_db)):
    db_user = _services.get_user_by_email(email=user.email, db=db)
    if db_user:
        raise HTTPException(status_code=400, detail="woops email already registered")
    return _services.create_user(user=user, db=db)


@app.post("/users/{user_id}/items/", response_model=_schemas.Item)
def create_item(
    user_id: int, item: _schemas.ItemCreate, db: Session = Depends(_services.get_db)
):
    db_user = _services.get_user(user_id=user_id, db=db)
    if db_user is None:
        raise HTTPException(
            status_code=404, detail=f"user with id ({user_id}) does not exist"
        )
    db_item = _services.create_item(user_id=user_id, item=item, db=db)
    return db_item


@app.get("/items/", response_model=List[_schemas.Item])
def get_items(skip: int = 0, limit: int = 10, db: Session = Depends(_services.get_db)):
    return _services.get_items(skip=skip, limit=limit, db=db)


@app.get("/items/{item_id}", response_model=_schemas.Item)
def get_item(item_id: int, db: Session = Depends(_services.get_db)):
    db_item = _services.get_item(item_id=item_id, db=db)
    if db_item is None:
        raise HTTPException(
            status_code=404, detail=f"item with item_id ({item_id}) does not exist"
        )
    return db_item


@app.put("/items/{item_id}", response_model=_schemas.Item)
def update_item(
    item_id: int, item: _schemas.ItemCreate, db: Session = Depends(_services.get_db)
):
    db_item = _services.get_item(item_id=item_id, db=db)
    if db_item is None:
        raise HTTPException(
            status_code=404, detail=f"item with item_id ({item_id}) does not exist"
        )
    return _services.update_item(item_id=item_id, item=item, db=db)


@app.delete("/items/{item_id}")
def delete_item(item_id, db: Session = Depends(_services.get_db)):
    _services.delete_item(item_id=item_id, db=db)
    return f"deleted item with item_id ({item_id})"
