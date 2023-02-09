# Run FastAPI server with:
# uvicorn inventory.main:app --reload

from fastapi import FastAPI
from redis_om import get_redis_connection, HashModel

app = FastAPI()

redis = get_redis_connection(
    host = "redis-10769.c55.eu-central-1-1.ec2.cloud.redislabs.com",
    port = 10769,
    password = "####",
    decode_responses = True
)

class Product(HashModel):
    name: str
    price: float
    quantity: int

@app.get("/")
async def root():
    return {"message": "Hello World"}