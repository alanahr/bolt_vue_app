from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv

from src.config.database import database
from src.routers import positions, entities, health
from src.middleware.rate_limit import RateLimitMiddleware

# Load environment variables
load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await database.connect()
    yield
    # Shutdown
    await database.disconnect()

# Create FastAPI app
app = FastAPI(
    title="Vue CRUD Backend API",
    description="A FastAPI backend for Vue CRUD application with MongoDB",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Environment configuration
NODE_ENV = os.getenv("NODE_ENV", "development")
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")

# Security middleware
app.add_middleware(
    TrustedHostMiddleware, 
    allowed_hosts=["*"] if NODE_ENV == "development" else ["localhost", "your-domain.com"]
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Compression middleware
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Rate limiting middleware
app.add_middleware(RateLimitMiddleware)

# Include routers
app.include_router(health.router, prefix="/health", tags=["health"])
app.include_router(positions.router, prefix="/api/positions", tags=["positions"])
app.include_router(entities.router, prefix="/api/entities", tags=["entities"])

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Vue CRUD Backend API",
        "version": "2.0.0",
        "environment": NODE_ENV,
        "docs": "/docs",
        "redoc": "/redoc"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=NODE_ENV == "development"
    )