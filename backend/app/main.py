from fastapi import FastAPI
from .db import Base, engine
from .routers import batches, inventory, sales, orders, chat, auth

app = FastAPI(title="Gigi Yogurt Backend")

# Defer table creation to startup to avoid import-time DB connection failures
@app.on_event("startup")
def on_startup() -> None:
    try:
        Base.metadata.create_all(bind=engine)
    except Exception as exc:  # pragma: no cover
        # Allow the app to start even if DB is unavailable (e.g., during smoke import)
        print(f"[startup] Warning: could not initialize database tables: {exc}")

app.include_router(batches.router)
app.include_router(inventory.router)
app.include_router(sales.router)
app.include_router(orders.router)
app.include_router(chat.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"service":"gigi-yogurt-backend","status":"ok"}
