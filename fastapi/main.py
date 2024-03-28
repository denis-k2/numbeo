import logging

import uvicorn
from fastapi import FastAPI

from api.router import router as api_router
from config import settings
from security.router import router as security_router
from utils import EndpointFilter, PrometheusMiddleware, metrics, setting_otlp

APP_NAME = settings.app_name
OTLP_GRPC_ENDPOINT = settings.otlp_grpc_endpoint
PROFILING = settings.profiling
RELO_HOST = settings.relo_host
RELO_PORT = settings.relo_port

app = FastAPI()

app.include_router(api_router)
app.include_router(security_router)

if PROFILING:
    from tests.profiling.middleware import PyInstrumentMiddleWare

    app.add_middleware(PyInstrumentMiddleWare)

# Setting metrics middleware
app.add_middleware(PrometheusMiddleware, app_name=APP_NAME)
app.add_route("/metrics", metrics)

# Setting OpenTelemetry exporter
setting_otlp(app, APP_NAME, OTLP_GRPC_ENDPOINT)


if __name__ == "__main__":
    # Filter out /endpoint
    logging.getLogger("uvicorn.access").addFilter(EndpointFilter())
    log_config = uvicorn.config.LOGGING_CONFIG
    log_config["formatters"]["access"]["fmt"] = (
        "%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] "
        "[trace_id=%(otelTraceID)s span_id=%(otelSpanID)s "
        "resource.service.name=%(otelServiceName)s] - %(message)s"
    )
    uvicorn.run(app, host=RELO_HOST, port=RELO_PORT, log_config=log_config)
