"""Main application entry point for Friendigami API using FastAPI."""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

import app.models  # noqa: F401 — register all SQLAlchemy models
from app.api import routes_combinations, routes_friends, routes_twilio
from app.db.base import Base, engine


@asynccontextmanager
async def lifespan(application: FastAPI):
    """Create database tables on startup."""
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="Friendigami API", lifespan=lifespan)

app.include_router(routes_friends.router)
app.include_router(routes_combinations.router)
app.include_router(routes_twilio.router)

# serve static SPA
app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/")
def read_root():
    """Serve the single-page UI."""
    return FileResponse("app/static/index.html")
