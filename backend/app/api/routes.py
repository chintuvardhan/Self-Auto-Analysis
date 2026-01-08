"""
API Routes for Data Analysis Application
Phase 1: File Upload & Dataset Profiling
Phase 2: Statistics Engine
Phase 3: Visualization Engine

This module defines all API endpoints:
- POST /api/upload: Upload CSV/Excel files
- GET /api/profile/{filename}: Get dataset profile
- GET /api/statistics/{filename}: Get dataset statistics
- GET /api/visualizations/{filename}: Get dataset visualizations
- GET /api/health: Health check endpoint
"""

from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from pathlib import Path
import shutil
import os

from app.services.profiler import DatasetProfiler
from app.services.statistics import StatisticsEngine
from app.services.visualizer import VisualizationEngine
from app.utils.validators import validate_file_extension

# Create API router
router = APIRouter()

# Get uploads directory path
UPLOADS_DIR = Path(__file__).parent.parent.parent / "uploads"


@router.get("/health")
async def health_check():
    """
    Health check endpoint to verify the API is running.
    
    Returns:
        dict: Status message
    """
    return {
        "status": "healthy",
        "message": "Data Analysis API is running",
        "phase": "1 - File Upload & Dataset Profiling"
    }


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    Upload a CSV or Excel file for analysis.
    
    Args:
        file: The uploaded file (CSV or Excel format)
    
    Returns:
        dict: Upload confirmation with filename and profile data
    
    Raises:
        HTTPException: If file type is invalid or upload fails
    """
    try:
        # Validate file extension
        if not validate_file_extension(file.filename):
            raise HTTPException(
                status_code=400,
                detail="Invalid file type. Only CSV and Excel files (.csv, .xlsx, .xls) are allowed."
            )
        
        # Ensure uploads directory exists
        UPLOADS_DIR.mkdir(exist_ok=True)
        
        # Save the uploaded file
        file_path = UPLOADS_DIR / file.filename
        
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Profile the dataset immediately after upload
        profiler = DatasetProfiler(str(file_path))
        profile_data = profiler.get_profile()
        
        return JSONResponse(
            status_code=200,
            content={
                "message": "File uploaded successfully",
                "filename": file.filename,
                "profile": profile_data
            }
        )
    
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    
    except Exception as e:
        # Handle unexpected errors
        raise HTTPException(
            status_code=500,
            detail=f"Error processing file: {str(e)}"
        )
    
    finally:
        # Close the file
        await file.close()


@router.get("/profile/{filename}")
async def get_profile(filename: str):
    """
    Get the profile of a previously uploaded dataset.
    
    Args:
        filename: Name of the uploaded file
    
    Returns:
        dict: Dataset profile information
    
    Raises:
        HTTPException: If file not found or profiling fails
    """
    try:
        file_path = UPLOADS_DIR / filename
        
        # Check if file exists
        if not file_path.exists():
            raise HTTPException(
                status_code=404,
                detail=f"File '{filename}' not found. Please upload the file first."
            )
        
        # Profile the dataset
        profiler = DatasetProfiler(str(file_path))
        profile_data = profiler.get_profile()
        
        return JSONResponse(
            status_code=200,
            content={
                "filename": filename,
                "profile": profile_data
            }
        )
    
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    
    except Exception as e:
        # Handle unexpected errors
        raise HTTPException(
            status_code=500,
            detail=f"Error profiling file: {str(e)}"
        )


@router.delete("/delete/{filename}")
async def delete_file(filename: str):
    """
    Delete an uploaded file.
    
    Args:
        filename: Name of the file to delete
    
    Returns:
        dict: Deletion confirmation
    
    Raises:
        HTTPException: If file not found or deletion fails
    """
    try:
        file_path = UPLOADS_DIR / filename
        
        # Check if file exists
        if not file_path.exists():
            raise HTTPException(
                status_code=404,
                detail=f"File '{filename}' not found."
            )
        
        # Delete the file
        os.remove(file_path)
        
        return JSONResponse(
            status_code=200,
            content={
                "message": "File deleted successfully",
                "filename": filename
            }
        )
    
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    
    except Exception as e:
        # Handle unexpected errors
        raise HTTPException(
            status_code=500,
            detail=f"Error deleting file: {str(e)}"
        )


@router.get("/statistics/{filename}")
async def get_statistics(filename: str):
    """
    Get descriptive statistics for a previously uploaded dataset.
    
    Phase 2: Statistics Engine
    Computes descriptive statistics for all numerical columns.
    
    Args:
        filename: Name of the uploaded file
    
    Returns:
        dict: Dataset statistics including:
            - dataset_summary: Overall statistics
            - column_statistics: Per-column statistics
    
    Raises:
        HTTPException: If file not found or statistics computation fails
    """
    try:
        file_path = UPLOADS_DIR / filename
        
        # Check if file exists
        if not file_path.exists():
            raise HTTPException(
                status_code=404,
                detail=f"File '{filename}' not found. Please upload the file first."
            )
        
        # Load the dataset and get profile
        profiler = DatasetProfiler(str(file_path))
        profile_data = profiler.get_profile()
        
        # Check if profiling was successful
        if profile_data.get('status') == 'error':
            raise HTTPException(
                status_code=500,
                detail=f"Error profiling dataset: {profile_data.get('error_message')}"
            )
        
        # Compute statistics
        stats_engine = StatisticsEngine(profiler.df, profile_data)
        statistics_data = stats_engine.get_statistics()
        
        # Handle case where no numerical columns exist
        if statistics_data.get('status') == 'no_numerical_columns':
            return JSONResponse(
                status_code=200,
                content={
                    "filename": filename,
                    "message": statistics_data.get('message'),
                    "dataset_summary": statistics_data.get('dataset_summary'),
                    "column_statistics": {}
                }
            )
        
        # Check if statistics computation was successful
        if statistics_data.get('status') == 'error':
            raise HTTPException(
                status_code=500,
                detail=f"Error computing statistics: {statistics_data.get('error_message')}"
            )
        
        return JSONResponse(
            status_code=200,
            content={
                "filename": filename,
                "dataset_summary": statistics_data.get('dataset_summary'),
                "column_statistics": statistics_data.get('column_statistics')
            }
        )
    
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    
    except Exception as e:
        # Handle unexpected errors
        raise HTTPException(
            status_code=500,
            detail=f"Error computing statistics: {str(e)}"
        )


@router.get("/visualizations/{filename}")
async def get_visualizations(filename: str):
    """
    Get visualizations for a previously uploaded dataset.
    
    Phase 3: Visualization Engine
    Generates charts automatically using rule-based logic.
    
    Args:
        filename: Name of the uploaded file
    
    Returns:
        dict: Visualization data including:
            - chart_count: Number of charts generated
            - charts: List of chart configurations
    
    Raises:
        HTTPException: If file not found or visualization generation fails
    """
    try:
        file_path = UPLOADS_DIR / filename
        
        # Check if file exists
        if not file_path.exists():
            raise HTTPException(
                status_code=404,
                detail=f"File '{filename}' not found. Please upload the file first."
            )
        
        # Load the dataset and get profile
        profiler = DatasetProfiler(str(file_path))
        profile_data = profiler.get_profile()
        
        # Check if profiling was successful
        if profile_data.get('status') == 'error':
            raise HTTPException(
                status_code=500,
                detail=f"Error profiling dataset: {profile_data.get('error_message')}"
            )
        
        # Get statistics (optional, for enhanced visualizations)
        try:
            stats_engine = StatisticsEngine(profiler.df, profile_data)
            statistics_data = stats_engine.get_statistics()
        except:
            statistics_data = None
        
        # Generate visualizations
        viz_engine = VisualizationEngine(profiler.df, profile_data, statistics_data)
        visualizations_data = viz_engine.get_visualizations()
        
        # Check if visualization generation was successful
        if visualizations_data.get('status') == 'error':
            raise HTTPException(
                status_code=500,
                detail=f"Error generating visualizations: {visualizations_data.get('error_message')}"
            )
        
        return JSONResponse(
            status_code=200,
            content={
                "filename": filename,
                "chart_count": visualizations_data.get('chart_count', 0),
                "charts": visualizations_data.get('charts', [])
            }
        )
    
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    
    except Exception as e:
        # Handle unexpected errors
        raise HTTPException(
            status_code=500,
            detail=f"Error generating visualizations: {str(e)}"
        )
