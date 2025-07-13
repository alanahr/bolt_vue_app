from fastapi import APIRouter, HTTPException, status
from typing import List
from src.models.position import Position, PositionCreate, PositionUpdate
from src.services.position_service import position_service

router = APIRouter()

@router.get("/", response_model=List[Position])
async def get_all_positions():
    """Get all positions"""
    try:
        positions = await position_service.get_all()
        return positions
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch positions: {str(e)}"
        )

@router.get("/{position_id}", response_model=Position)
async def get_position(position_id: int):
    """Get position by ID"""
    try:
        position = await position_service.get_by_id(position_id)
        if not position:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Position not found"
            )
        return position
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch position: {str(e)}"
        )

@router.post("/", response_model=Position, status_code=status.HTTP_201_CREATED)
async def create_position(position_data: PositionCreate):
    """Create a new position"""
    try:
        position = await position_service.create(position_data)
        return position
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create position: {str(e)}"
        )

@router.put("/{position_id}", response_model=Position)
async def update_position(position_id: int, position_data: PositionUpdate):
    """Update a position"""
    try:
        position = await position_service.update(position_id, position_data)
        if not position:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Position not found"
            )
        return position
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update position: {str(e)}"
        )

@router.delete("/{position_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_position(position_id: int):
    """Delete a position"""
    try:
        deleted = await position_service.delete(position_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Position not found"
            )
        return None
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete position: {str(e)}"
        )