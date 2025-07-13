from typing import List, Optional
from src.config.database import database
from src.models.entity import Entity, EntityCreate, EntityUpdate
from datetime import datetime

class EntityService:
    def __init__(self):
        self.collection_name = "entities"

    async def get_next_id(self) -> int:
        """Get the next available ID"""
        db = database.get_db()
        last_entity = await db[self.collection_name].find_one(
            {}, sort=[("id", -1)]
        )
        return last_entity["id"] + 1 if last_entity else 1

    async def get_all(self) -> List[Entity]:
        """Get all entities"""
        db = database.get_db()
        cursor = db[self.collection_name].find({}).sort("id", 1)
        entities = []
        async for doc in cursor:
            # Remove MongoDB _id field
            doc.pop("_id", None)
            entities.append(Entity(**doc))
        return entities

    async def get_by_id(self, entity_id: int) -> Optional[Entity]:
        """Get entity by ID"""
        db = database.get_db()
        doc = await db[self.collection_name].find_one({"id": entity_id})
        if not doc:
            return None
        
        # Remove MongoDB _id field
        doc.pop("_id", None)
        return Entity(**doc)

    async def create(self, entity_data: EntityCreate) -> Entity:
        """Create a new entity"""
        db = database.get_db()
        entity_id = await self.get_next_id()
        
        entity_dict = entity_data.model_dump()
        entity_dict.update({
            "id": entity_id,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        })
        
        result = await db[self.collection_name].insert_one(entity_dict)
        if not result.inserted_id:
            raise Exception("Failed to create entity")
        
        return Entity(**entity_dict)

    async def update(self, entity_id: int, entity_data: EntityUpdate) -> Optional[Entity]:
        """Update an entity"""
        db = database.get_db()
        
        # Only update fields that are provided
        update_data = {k: v for k, v in entity_data.model_dump().items() if v is not None}
        if not update_data:
            return await self.get_by_id(entity_id)
        
        update_data["updated_at"] = datetime.now()
        
        result = await db[self.collection_name].find_one_and_update(
            {"id": entity_id},
            {"$set": update_data},
            return_document=True
        )
        
        if not result:
            return None
        
        # Remove MongoDB _id field
        result.pop("_id", None)
        return Entity(**result)

    async def delete(self, entity_id: int) -> bool:
        """Delete an entity"""
        db = database.get_db()
        result = await db[self.collection_name].delete_one({"id": entity_id})
        return result.deleted_count > 0

# Create singleton instance
entity_service = EntityService()