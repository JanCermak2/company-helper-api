import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from .database import engine
from .models import Base
from .routers.tickets import router as tickets_router
from .routers.reports import router as reports_router
from .logging_config import setup_logging

logger = logging.getLogger("app")

app = FastAPI(title="Company Helper API")


@app.on_event("startup")
def on_startup():
    setup_logging()
    Base.metadata.create_all(bind=engine)
    logger.info("Startup complete")


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.warning("Validation error on %s: %s", request.url.path, exc.errors())
    return JSONResponse(
        status_code=422,
        content={
            "error": {
                "type": "validation_error",
                "message": "Invalid request",
                "details": exc.errors(),
            }
        },
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled error on %s", request.url.path)
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "type": "internal_error",
                "message": "Unexpected server error",
            }
        },
    )


app.include_router(tickets_router)
app.include_router(reports_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
