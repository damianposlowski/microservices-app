# Run FastAPI server with:
# uvicorn inventory.main:app --reload

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}