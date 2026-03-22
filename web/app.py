"""
OftalmoClaw - FastAPI Web Application (Mission Control)
Created by GeekVision
"""

import logging
import time
from collections import defaultdict
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from pathlib import Path

from config import settings
from models.database import init_db
from web.routes import dashboard, cases, analytics, api

# ---- Logging ----
logging.basicConfig(
    level=getattr(logging, settings.log_level.upper(), logging.INFO),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("logs/oftalmo.log", encoding="utf-8"),
    ],
)
logger = logging.getLogger("oftalmo")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("OftalmoClaw v%s starting...", settings.app_version)
    await init_db()
    logger.info("Database initialized")
    yield
    logger.info("OftalmoClaw shutting down")


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    lifespan=lifespan,
    docs_url=None if not settings.debug else "/docs",
    redoc_url=None,
)

# ---- CORS Policy ----
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8000",
        "http://127.0.0.1:8000",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "DELETE"],
    allow_headers=["Content-Type"],
)

# ---- Rate Limiting (in-memory, per-IP) ----
_rate_limits: dict = defaultdict(list)
RATE_LIMIT_CHAT = 20       # max requests per window
RATE_LIMIT_API = 60         # max requests per window
RATE_LIMIT_WINDOW = 60      # seconds


@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    """Simple in-memory rate limiter per IP."""
    path = request.url.path
    client_ip = request.client.host if request.client else "unknown"

    # Only rate limit API routes
    if path.startswith("/api/"):
        now = time.time()
        key = f"{client_ip}:{path}"

        # Use stricter limit for chat (LLM calls cost money)
        limit = RATE_LIMIT_CHAT if "/chat" in path else RATE_LIMIT_API

        # Clean old entries
        _rate_limits[key] = [t for t in _rate_limits[key] if now - t < RATE_LIMIT_WINDOW]

        if len(_rate_limits[key]) >= limit:
            logger.warning("Rate limit exceeded: %s from %s", path, client_ip)
            return JSONResponse(
                status_code=429,
                content={"detail": "Muitas requisições. Tente novamente em alguns segundos."},
            )

        _rate_limits[key].append(now)

    response = await call_next(request)
    return response


# ---- Request Logging ----
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log API requests with timing."""
    if request.url.path.startswith("/api/"):
        start = time.time()
        response = await call_next(request)
        duration = round((time.time() - start) * 1000)
        logger.info(
            "%s %s %s %dms",
            request.method,
            request.url.path,
            response.status_code,
            duration,
        )
        return response
    return await call_next(request)


# ---- Global Error Handler ----
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Catch unhandled exceptions and return JSON error."""
    logger.error("Unhandled error on %s: %s", request.url.path, str(exc), exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Erro interno do servidor. Tente novamente."},
    )


# Static files and templates
static_dir = Path(__file__).parent / "static"
templates_dir = Path(__file__).parent / "templates"

app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")
templates = Jinja2Templates(directory=str(templates_dir))


# Health check
@app.get("/health")
async def health():
    return {"status": "ok", "app": settings.app_name, "version": settings.app_version}


# Main routes (no login required)
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "title": "Mission Control",
        "app_name": settings.app_name,
        "version": settings.app_version,
    })


@app.get("/second-opinion", response_class=HTMLResponse)
async def second_opinion_page(request: Request):
    return templates.TemplateResponse("second_opinion.html", {
        "request": request,
        "title": "Segunda Opinião",
        "app_name": settings.app_name,
    })


@app.get("/trends", response_class=HTMLResponse)
async def trends_page(request: Request):
    return templates.TemplateResponse("trends.html", {
        "request": request,
        "title": "Tendências",
        "app_name": settings.app_name,
    })


@app.get("/calculators", response_class=HTMLResponse)
async def calculators_page(request: Request):
    return templates.TemplateResponse("calculators.html", {
        "request": request,
        "title": "Calculadoras",
        "app_name": settings.app_name,
    })


@app.get("/chat", response_class=HTMLResponse)
async def chat_page(request: Request):
    return templates.TemplateResponse("chat.html", {
        "request": request,
        "title": "Chat IA",
        "app_name": settings.app_name,
    })


# Include API routers
app.include_router(dashboard.router, prefix="/api/v1/dashboard", tags=["dashboard"])
app.include_router(cases.router, prefix="/api/v1/cases", tags=["cases"])
app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["analytics"])
app.include_router(api.router, prefix="/api/v1", tags=["general"])
