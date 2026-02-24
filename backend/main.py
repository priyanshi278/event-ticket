from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import auth, admin, organizer, customer, entry_manager, support, offers
from database.database import engine, Base
import models 

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Event Ticket Booking Platform API",
    description="A centralized system to manage events, bookings, payments, and support.",
    version="1.0.0"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(organizer.router)
app.include_router(customer.router)
app.include_router(entry_manager.router)
app.include_router(support.router)
app.include_router(offers.router)

@app.get("/")
def root():
    return {"message": "Welcome to the Event Ticket Booking Platform API"}
