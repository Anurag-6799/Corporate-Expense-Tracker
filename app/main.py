from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.db.database import engine, Base
from app.api import auth, users, expenses

# 1. Initialize Database Tables
Base.metadata.create_all(bind=engine)

# 2. Initialize the FastAPI Application
app = FastAPI(title=settings.PROJECT_NAME)

# 3. Configure CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 4. Register the API Routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(expenses.router)

# 5. Root Health Check
@app.get("/")
def health_check():
    return {"status": "healthy", "service": settings.PROJECT_NAME}

