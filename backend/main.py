from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
import uvicorn

from backend.config.settings import get_settings
from backend.database.database import init_db
from backend.utils.logger import app_logger
from backend.api.routes.leads import router as leads_router

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Modern lifespan handler (replaces deprecated on_event)."""
    app_logger.info("Initializing database...")
    init_db()
    app_logger.info("Database initialized successfully.")
    yield
    # Shutdown logic here if needed


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS if isinstance(settings.CORS_ORIGINS, list) else [settings.CORS_ORIGINS],
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)

# Include leads router
app.include_router(leads_router, prefix=settings.API_PREFIX + "/leads")


# Health check
@app.get("/health", tags=["health"])
@app.get("/api/v1/health", tags=["health"])
async def health_check():
    return {"status": "healthy", "app": settings.APP_NAME, "version": settings.APP_VERSION}


# Custom validation error handler
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    app_logger.warning(f"Validation error: {exc.errors()}")
    has_invalid_value = any(e.get("type") != "missing" for e in exc.errors())
    status_code = 400 if has_invalid_value else 422
    error_details = []
    for err in exc.errors():
        loc = " -> ".join(str(l) for l in err.get("loc", []))
        msg = err.get("msg", "Value error")
        error_details.append(f"{loc}: {msg}")
    return JSONResponse(
        status_code=status_code,
        content={"detail": "; ".join(error_details), "errors": exc.errors()},
    )


if __name__ == "__main__":
    uvicorn.run("backend.main:app", host=settings.HOST, port=settings.PORT, reload=settings.RELOAD)
