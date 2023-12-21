from pyinstrument import Profiler
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from config import settings

INTERVAL = settings.interval
ASYNC_MODE = settings.async_mode


def convert_url(request: Request) -> str:
    path = request.get("path").lstrip("/").replace("/", "_").lower()
    query = request.get("query_string")
    if len(query) > 0:
        return path + "-" + query.decode().replace("=true", "").lower()
    return path


class PyInstrumentMiddleWare(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        file_name = convert_url(request)
        profiler = Profiler(interval=INTERVAL, async_mode=ASYNC_MODE)
        profiler.start()
        response = await call_next(request)
        profiler.stop()
        # Write result to html file
        profiler.write_html(f"./tests/profiling/sync_code_reports/{file_name}.html")
        return response
