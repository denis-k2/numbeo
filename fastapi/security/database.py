from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = os.environ.get("DATABASE_URL")
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:5123@localhost:5432/security"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    with SessionLocal() as session:
        yield session
