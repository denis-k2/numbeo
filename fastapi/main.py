from fastapi import FastAPI

from api.router import router as api_router
from security.router import router as security_router

app = FastAPI()

app.include_router(api_router)
app.include_router(security_router)
