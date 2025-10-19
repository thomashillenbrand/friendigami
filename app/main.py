"""Main application entry point for Friendigami API using FastAPI."""
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.api import routes_friends

app = FastAPI(title="Friendigami API")

app.include_router(routes_friends.router)

# serve static SPA
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/")
def read_root():
    # serve the single-page UI
    return FileResponse("app/static/indexv2.html")