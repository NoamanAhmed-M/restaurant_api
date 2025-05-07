from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes import users, clients, reservations, tables, menu, orders, payments, inventory, auth

app = FastAPI(
    title="Restaurant Management API",
    description="A modular API backend for restaurant operations",
    version="1.2"
)

# CORS settings (allow all origins for development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(clients.router)
app.include_router(reservations.router)
app.include_router(tables.router)
app.include_router(menu.router)
app.include_router(orders.router)
app.include_router(payments.router)
app.include_router(inventory.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Restaurant API v1.2"}