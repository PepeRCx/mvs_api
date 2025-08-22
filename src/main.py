from fastapi import FastAPI
from server.v1 import router as api_v1_router
from database import start_db

app = FastAPI()

start_db()


@app.get("/")
def root():
    return {"version": "1.0.0", "author": "pepe"}


app.include_router(api_v1_router, prefix="/api/v1")
