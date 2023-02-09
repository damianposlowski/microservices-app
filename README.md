This is a project to create a simple microservices app with Python, FastAPI, JavaScript and React.

I used RedisJSON as a Database and Redis Streams to dispatch events.

The app is divided into two parts:
- inventory
- payment

It's a microservice allowing to manage inventory supplies, buy these supplies with a payment system that additionally adds provision and update the inventory after each transaction.