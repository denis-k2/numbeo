from fastapi import FastAPI
import router
from database import engine, get_db
from models import Base

# delegate to Alembic
Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(router.router)
