from fastapi import FastAPI

from api.router import router as api_router
from config import settings
from security.router import router as security_router

PROFILING = settings.profiling

app = FastAPI()

app.include_router(api_router)
app.include_router(security_router)

if PROFILING:
    from tests.profiling.middleware import PyInstrumentMiddleWare

    app.add_middleware(PyInstrumentMiddleWare)
