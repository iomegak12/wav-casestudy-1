import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

CONNECTION_STRING = os.environ["DB_CONNECTION_STRING"]

engine = create_engine(CONNECTION_STRING,
                       connect_args={
                           "check_same_thread": False
                       },
                       echo=True)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
