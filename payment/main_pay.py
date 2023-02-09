# Run FastAPI server with:
# uvicorn payment.main_pay:app --reload --port=8001

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.background import BackgroundTasks
from redis_om import get_redis_connection, HashModel
from starlette.requests import Request
import requests
import time

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["http://localhost:3000"],
    allow_methods = ["*"],
    allow_headers = ["*"]
)

redis = get_redis_connection(
    host = "redis-10769.c55.eu-central-1-1.ec2.cloud.redislabs.com",
    port = 10769,
    password = "####",
    decode_responses = True
)

class Order(HashModel):
    product_id: str
    price: float
    fee: float
    total: float
    quantity: int
    status: str

    class Meta:
        database = redis

@app.get("/orders/{pk}")
def get(pk: str):
    return Order.get(pk)

@app.post("/orders")
async def create(request: Request, background_tasks: BackgroundTasks):
    body = await request.json()
    id = body["id"]
    req = requests.get(f"http://localhost:8000/products/{id}")
    product = req.json()

    order = Order(
        product_id = body['id'],
        price = product['price'],
        fee = 0.35 * product['price'],
        total = 1.35 * product['price'],
        quantity = body['quantity'],
        status = 'pending'
    )
    order.save()
    
    background_tasks.add_task(order_completed, order)
    return order

def order_completed(order: Order):
    time.sleep(3)
    order.status = "completed"
    order.save()
    redis.xadd("order_completed", order.dict(), "*")