from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime

class DetailBase(BaseModel):
    id: int = Field(..., description="Detail ID")
    name: str = Field(..., min_length=1, description="Detail name")
    description: Optional[Dict[str, Any]] = Field({}, description="TipTap editor content")
    tags: List[Dict[str, Any]] = Field([], description="Associated entity tags")
    details: List['DetailBase'] = Field([], description="Nested details")

# Enable forward references
DetailBase.model_rebuild()

class PositionBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200, description="Position title")
    start_year: int = Field(..., ge=1900, le=2100, description="Start year")
    start_month: int = Field(..., ge=1, le=12, description="Start month")
    start_day: int = Field(..., ge=1, le=31, description="Start day")
    end_year: Optional[int] = Field(None, ge=1900, le=2100, description="End year")
    end_month: Optional[int] = Field(None, ge=1, le=12, description="End month")
    end_day: Optional[int] = Field(None, ge=1, le=31, description="End day")
    salary: Optional[float] = Field(None, ge=0, description="Salary amount")
    details: List[DetailBase] = Field([], description="Position details")

    @validator('end_year')
    def validate_end_year(cls, v, values):
        if v is not None and 'start_year' in values and v < values['start_year']:
            raise ValueError('End year must be greater than or equal to start year')
        return v

class PositionCreate(PositionBase):
    pass

class PositionUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    start_year: Optional[int] = Field(None, ge=1900, le=2100)
    start_month: Optional[int] = Field(None, ge=1, le=12)
    start_day: Optional[int] = Field(None, ge=1, le=31)
    end_year: Optional[int] = Field(None, ge=1900, le=2100)
    end_month: Optional[int] = Field(None, ge=1, le=12)
    end_day: Optional[int] = Field(None, ge=1, le=31)
    salary: Optional[float] = Field(None, ge=0)
    details: Optional[List[DetailBase]] = None

class Position(PositionBase):
    id: int = Field(..., description="Unique position ID")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Senior Software Engineer",
                "start_year": 2022,
                "start_month": 1,
                "start_day": 15,
                "end_year": None,
                "end_month": None,
                "end_day": None,
                "salary": 120000.0,
                "details": [],
                "created_at": "2024-01-01T00:00:00",
                "updated_at": "2024-01-01T00:00:00"
            }
        }