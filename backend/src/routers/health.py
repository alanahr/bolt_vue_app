from fastapi import APIRouter, HTTPException, status
from src.config.database import database
import psutil
import os
from datetime import datetime

router = APIRouter()

@router.get("/")
async def health_check():
    """Health check endpoint"""
    try:
        # Check database connection
        db_status = "connected" if database.is_ready() else "disconnected"
        db_info = {"status": db_status}
        
        if database.is_ready():
            try:
                db = database.get_db()
                await db.command("ping")
                db_info["ping"] = "success"
            except Exception as e:
                db_info["ping"] = "failed"
                db_info["error"] = str(e)
        
        # System information
        memory = psutil.virtual_memory()
        cpu_percent = psutil.cpu_percent(interval=1)
        
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "uptime": psutil.boot_time(),
            "system": {
                "cpu_percent": cpu_percent,
                "memory": {
                    "total": memory.total,
                    "available": memory.available,
                    "percent": memory.percent
                },
                "python_version": os.sys.version
            },
            "database": db_info,
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "status": "unhealthy",
                "timestamp": datetime.now().isoformat(),
                "error": str(e)
            }
        )