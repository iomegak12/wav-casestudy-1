from sqlalchemy.orm import Session
from . import models, schemas


class ItemRepository:
    async def create(db: Session, item: schemas.ItemCreate):
        db_item = models.Item(
            name=item.name,
            description=item.description,
            price=item.price,
            store_id=item.store_id
        )

        db.add(db_item)
        db.commit()
        db.refresh(db_item)

        return db_item

    def fetch_by_id(db: Session, _id):
        return db.query(models.Item)\
            .filter(models.Item.id == _id)\
            .first()

    def fetch_by_name(db: Session, name):
        return db.query(models.Item)\
            .filter(models.Item.name == name)\
            .first()

    def fetch_all(db: Session, skip: int = 0, limit: int = 10):
        return db.query(models.Item)\
            .offset(skip)\
            .limit(limit)\
            .all()
