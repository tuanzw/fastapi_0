from sqlalchemy.orm import Session
from datetime import datetime

import database as _database, models as _models, schemas as _schemas


def create_database():
    return _database.Base.metadata.create_all(bind=_database.engine)


def get_db():
    db = _database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_users(skip: int, limit: int, db: Session):
    return db.query(_models.User).offset(skip).limit(limit).all()


def get_user(user_id: int, db: Session):
    return db.query(_models.User).filter(_models.User.id == user_id).first()


def get_user_by_email(email: str, db: Session):
    return db.query(_models.User).filter(_models.User.email == email).first()


def create_user(user: _schemas.UserCreate, db: Session):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = _models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_item(user_id: int, item: _schemas.ItemCreate, db: Session):
    db_item = _models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_items(skip: int, limit: int, db: Session):
    return db.query(_models.Item).offset(skip).limit(limit).all()


def get_item(item_id, db: Session):
    return db.query(_models.Item).filter(_models.Item.id == item_id).first()


def update_item(item_id: int, item: _schemas.ItemCreate, db: Session):
    db_item = get_item(item_id=item_id, db=db)
    db_item.title = item.title
    db_item.description = item.description
    db_item.date_last_updated = datetime.now()
    db.commit()
    db.refresh(db_item)
    return db_item


def delete_item(item_id: int, db: Session):
    db.query(_models.Item).filter(_models.Item.id == item_id).delete()
    db.commit()
