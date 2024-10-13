import time
import asyncio

from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from warehouse.common import Base, engine, get_db
from warehouse.items import ItemRepository, Item, ItemCreate
from warehouse.stores import StoreRepository, Store, StoreCreate

app = FastAPI(
    title="WAV - Warehouse API",
    description="Simple FastAPI REST Service to manage Stores and Items",
    version="1.0"
)

Base.metadata.create_all(bind=engine)


@app.exception_handler(Exception)
def validate_exception_handle(request, error):
    base_error_message = f"Failed to Handle the Request and Execute: {
        request.method}: {request.url}"

    return JSONResponse(
        status_code=400,
        content={
            "message": f"{base_error_message}, Detail :{error}"
        }
    )


@app.middleware("http")
async def add_process_time_header(request, call_next):
    print("Inside the Middleware ...")

    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time

    response.headers["X-Process-Time"] = str(f"{process_time:0.4f} Second(s)")

    return response


@app.post("/items",
          tags=["Item"],
          response_model=Item,
          status_code=201)
async def create_item(item_request: ItemCreate, db: Session = Depends(get_db)):
    """
        Create an Item and store it in the Database
    """

    db_item = ItemRepository.fetch_by_name(db, name=item_request.name)

    if db_item:
        raise HTTPException(
            status_code=400,
            detail="Item Already Exists!"
        )

    return await ItemRepository.create(db=db, item=item_request)


@app.get("/items",
         tags=["Item"],
         response_model=List[Item])
def get_all_items(name: Optional[str] = None, db: Session = Depends(get_db)):
    """
        Gets All Items stored in the database, Optionally Specify the name of the Item to Retrieve Specific Item
    """

    if name:
        items = []
        db_item = ItemRepository.fetch_by_name(db, name)
        items.append(db_item)
    else:
        items = ItemRepository.fetch_all(db)

    return items


@app.get("/items/{item_id}",
         tags=["Item"],
         response_model=Item)
def get_item(item_id: int, db: Session = Depends(get_db)):
    """
        Gets the item with the Given Item ID
    """

    db_item = ItemRepository.fetch_by_id(db, item_id)

    if db_item is None:
        raise HTTPException(
            status_code=404,
            detail="Item Not Found!"
        )

    return db_item


@app.post("/stores",
          tags=["Store"],
          response_model=Store,
          status_code=201)
async def create_store(store_request: StoreCreate, db: Session = Depends(get_db)):
    """
        Create an store and save it in the Database
    """

    db_store = StoreRepository.fetch_by_name(db, name=store_request.name)

    if db_store:
        raise HTTPException(
            status_code=400,
            detail="store Already Exists!"
        )

    return await StoreRepository.create(db=db, store=store_request)


@app.get("/stores",
         tags=["Store"],
         response_model=List[Store])
def get_all_stores(name: Optional[str] = None, db: Session = Depends(get_db)):
    """
        Gets All stores stored in the database, Optionally Specify the name of the store to Retrieve Specific store
    """

    if name:
        stores = []
        db_store = StoreRepository.fetch_by_name(db, name)
        stores.append(db_store)
    else:
        stores = StoreRepository.fetch_all(db)

    return stores


@app.get("/stores/{store_id}",
         tags=["Store"],
         response_model=Store)
def get_store(store_id: int, db: Session = Depends(get_db)):
    """
        Gets the store with the Given store ID
    """

    db_store = StoreRepository.fetch_by_id(db, store_id)

    if db_store is None:
        raise HTTPException(
            status_code=404,
            detail="store Not Found!"
        )

    return db_store
