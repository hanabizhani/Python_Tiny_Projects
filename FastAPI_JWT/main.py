from fastapi import FastAPI
from app.auth.api import router as auth_router

# Initialize the FastAPI app
app = FastAPI()
# Include the router from api_.py
# app.include_router(auth_router, prefix="/auth")
@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

