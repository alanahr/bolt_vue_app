from typing import List, Optional
from src.config.database import database
from src.models.position import Position, PositionCreate, PositionUpdate
from datetime import datetime

class PositionService:
    def __init__(self):
        self.collection_name = "positions"

    async def get_next_id(self) -> int:
        """Get the next available ID"""
        db = database.get_db()
        last_position = await db[self.collection_name].find_one(
            {}, sort=[("id", -1)]
        )
        return last_position["id"] + 1 if last_position else 1

    async def get_all(self) -> List[Position]:
        """Get all positions"""
        db = database.get_db()
        cursor = db[self.collection_name].find({}).sort("id", 1)
        positions = []
        async for doc in cursor:
            # Remove MongoDB _id field
            doc.pop("_id", None)
            positions.append(Position(**doc))
        return positions

    async def get_by_id(self, position_id: int) -> Optional[Position]:
        """Get position by ID"""
        db = database.get_db()
        doc = await db[self.collection_name].find_one({"id": position_id})
        if not doc:
            return None
        
        # Remove MongoDB _id field
        doc.pop("_id", None)
        return Position(**doc)

    async def create(self, position_data: PositionCreate) -> Position:
        """Create a new position"""
        db = database.get_db()
        position_id = await self.get_next_id()
        
        position_dict = position_data.model_dump()
        position_dict.update({
            "id": position_id,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        })
        
        result = await db[self.collection_name].insert_one(position_dict)
        if not result.inserted_id:
            raise Exception("Failed to create position")
        
        return Position(**position_dict)

    async def update(self, position_id: int, position_data: PositionUpdate) -> Optional[Position]:
        """Update a position"""
        db = database.get_db()
        
        # Only update fields that are provided
        update_data = {k: v for k, v in position_data.model_dump().items() if v is not None}
        if not update_data:
            return await self.get_by_id(position_id)
        
        update_data["updated_at"] = datetime.now()
        
        result = await db[self.collection_name].find_one_and_update(
            {"id": position_id},
            {"$set": update_data},
            return_document=True
        )
        
        if not result:
            return None
        
        # Remove MongoDB _id field
        result.pop("_id", None)
        return Position(**result)

    async def delete(self, position_id: int) -> bool:
        """Delete a position"""
        db = database.get_db()
        result = await db[self.collection_name].delete_one({"id": position_id})
        return result.deleted_count > 0

# Create singleton instance
position_service = PositionService()