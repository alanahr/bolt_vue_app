from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class EntityBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Entity name")
    entity_type: str = Field(
        ..., 
        regex="^(company|person|skill|location|room|container|equipment|muscles|meta|exercise_type|object|tool|other)$",
        description="Type of entity"
    )
    entity_parent: Optional[int] = Field(None, description="Parent entity ID")
    color: Optional[str] = Field("", max_length=7, description="Color code (hex)")
    icon: Optional[str] = Field("", max_length=50, description="Icon class name")

class EntityCreate(EntityBase):
    pass

class EntityUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    entity_type: Optional[str] = Field(
        None, 
        regex="^(company|person|skill|location|room|container|equipment|muscles|meta|exercise_type|object|tool|other)$"
    )
    entity_parent: Optional[int] = None
    color: Optional[str] = Field(None, max_length=7)
    icon: Optional[str] = Field(None, max_length=50)

class Entity(EntityBase):
    id: int = Field(..., description="Unique entity ID")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Python",
                "entity_type": "skill",
                "entity_parent": None,
                "color": "#3776ab",
                "icon": "fab fa-python",
                "created_at": "2024-01-01T00:00:00",
                "updated_at": "2024-01-01T00:00:00"
            }
        }