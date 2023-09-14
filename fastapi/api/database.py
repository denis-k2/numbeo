from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import settings

SQLALCHEMY_RELOHELPER_URL = settings.relohelper_url

engine = create_engine(SQLALCHEMY_RELOHELPER_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    with SessionLocal() as session:
        yield session
