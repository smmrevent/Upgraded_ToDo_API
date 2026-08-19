from fastapi import FastAPI
from database import Base, engine
from routers import auth

app = FastAPI(title="Upgraded", version="1.1")

app.include_router(auth.router)

@app.get("/health")
async def get_health():
    return {"Status": "200 OK"}