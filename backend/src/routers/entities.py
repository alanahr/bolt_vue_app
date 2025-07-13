from fastapi import APIRouter, HTTPException, status
from typing import List
from src.models.entity import Entity, EntityCreate, EntityUpdate
from src.services.entity_service import entity_service

router = APIRouter()

@router.get("/", response_model=List[Entity])
async def get_all_entities():
    """Get all entities"""
    try:
        entities = await entity_service.get_all()
        return entities
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch entities: {str(e)}"
        )

@router.get("/{entity_id}", response_model=Entity)
async def get_entity(entity_id: int):
    """Get entity by ID"""
    try:
        entity = await entity_service.get_by_id(entity_id)
        if not entity:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Entity not found"
            )
        return entity
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch entity: {str(e)}"
        )

@router.post("/", response_model=Entity, status_code=status.HTTP_201_CREATED)
async def create_entity(entity_data: EntityCreate):
    """Create a new entity"""
    try:
        entity = await entity_service.create(entity_data)
        return entity
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create entity: {str(e)}"
        )

@router.put("/{entity_id}", response_model=Entity)
async def update_entity(entity_id: int, entity_data: EntityUpdate):
    """Update an entity"""
    try:
        entity = await entity_service.update(entity_id, entity_data)
        if not entity:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Entity not found"
            )
        return entity
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update entity: {str(e)}"
        )

@router.delete("/{entity_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_entity(entity_id: int):
    """Delete an entity"""
    try:
        deleted = await entity_service.delete(entity_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Entity not found"
            )
        return None
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete entity: {str(e)}"
        )