from fastapi import FastAPI
from .db import Base, engine
from .routers import batches, inventory, sales, orders, chat, auth

# create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Gigi Yogurt Backend" )

app.include_router(batches.router)
app.include_router(inventory.router)
app.include_router(sales.router)
app.include_router(orders.router)
app.include_router(chat.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"service":"gigi-yogurt-backend","status":"ok"}
