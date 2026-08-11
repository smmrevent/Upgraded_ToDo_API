from fastapi import FastAPI

app = FastAPI(title="Upgraded", version="1.1")

@app.get("/health")
async def get_health():
    return {"Status": "200 OK"}