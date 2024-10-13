from sqlalchemy.orm import Session
from . import models, schemas


class StoreRepository:
    async def create(db: Session, store: schemas.StoreCreate):
        db_store = models.Store(name=store.name)

        db.add(db_store)
        db.commit()
        db.refresh(db_store)

        return db_store

    def fetch_by_id(db: Session, _id: int):
        return db.query(models.Store)\
            .filter(models.Store.id == _id)\
            .first()

    def fetch_by_name(db: Session, name: str):
        return db.query(models.Store)\
            .filter(models.Store.name == name)\
            .first()

    def fetch_all(db: Session, skip: int = 0, limit: int = 10):
        return db.query(models.Store)\
            .offset(skip)\
            .limit(limit)\
            .all()
