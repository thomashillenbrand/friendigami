from fastapi import FastAPI
from app.api import routes_friends

app = FastAPI(title="Friendigami API")

app.include_router(routes_friends.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Friendigami API!"}