"""
OftalmoClaw - FastAPI Web Application (Mission Control)
Created by GeekVision
"""

from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from contextlib import asynccontextmanager
from pathlib import Path

from config import settings
from models.database import init_db
from web.routes import dashboard, cases, analytics, api


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    lifespan=lifespan,
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


# Main routes
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
        "title": "Segunda Opiniao",
        "app_name": settings.app_name,
    })


@app.get("/trends", response_class=HTMLResponse)
async def trends_page(request: Request):
    return templates.TemplateResponse("trends.html", {
        "request": request,
        "title": "Dashboard de Tendencias",
        "app_name": settings.app_name,
    })


@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {
        "request": request,
        "title": "Login",
        "app_name": settings.app_name,
    })


# Include API routers
app.include_router(dashboard.router, prefix="/api/v1/dashboard", tags=["dashboard"])
app.include_router(cases.router, prefix="/api/v1/cases", tags=["cases"])
app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["analytics"])
app.include_router(api.router, prefix="/api/v1", tags=["general"])
