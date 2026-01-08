"""
FastAPI Application Entry Point
Phase 1: File Upload & Dataset Profiling

This module initializes the FastAPI application with:
- CORS middleware for cross-origin requests
- Static file serving for the frontend
- API route registration
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import os

from app.api.routes import router

# Initialize FastAPI application
app = FastAPI(
    title="Data Analysis Web Application",
    description="A rule-based data analysis system with no AI APIs - Phases 1, 2 & 3",
    version="3.0.0",
    docs_url="/api/docs",  # Swagger UI
    redoc_url="/api/redoc"  # ReDoc
)

# Configure CORS to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routes
app.include_router(router, prefix="/api")

# Serve static frontend files
frontend_path = Path(__file__).parent.parent.parent / "frontend"
if frontend_path.exists():
    app.mount("/", StaticFiles(directory=str(frontend_path), html=True), name="frontend")

# Create uploads directory if it doesn't exist
uploads_dir = Path(__file__).parent.parent / "uploads"
uploads_dir.mkdir(exist_ok=True)


@app.on_event("startup")
async def startup_event():
    """
    Application startup event handler.
    Performs initialization tasks when the server starts.
    """
    print("=" * 60)
    print("Data Analysis Web Application - Backend Server")
    print("Phase 1: File Upload & Dataset Profiling")
    print("Phase 2: Statistics Engine")
    print("Phase 3: Visualization Engine")
    print("=" * 60)
    print(f"Uploads directory: {uploads_dir}")
    print(f"Frontend directory: {frontend_path}")
    print("Server is ready to accept requests!")
    print("=" * 60)


@app.on_event("shutdown")
async def shutdown_event():
    """
    Application shutdown event handler.
    Cleanup tasks when the server stops.
    """
    print("\nShutting down server...")
