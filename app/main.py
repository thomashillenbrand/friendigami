"""Main application entry point for Friendigami API using FastAPI."""
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

import app.models  # noqa: F401 — register all SQLAlchemy models
from app.api import routes_combinations, routes_friends, routes_twilio

app = FastAPI(title="Friendigami API")

app.include_router(routes_friends.router)
app.include_router(routes_combinations.router)
app.include_router(routes_twilio.router)

# serve static SPA
app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/")
def read_root():
    """Serve the single-page UI."""
    return FileResponse("app/static/index.html")
