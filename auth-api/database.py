from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, Session
from models import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///./Users.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base.metadata.create_all(bind=engine)


async def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
