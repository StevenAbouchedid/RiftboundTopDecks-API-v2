"""Format schemas"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime


class FormatSetResponse(BaseModel):
    """Schema for format set response"""
    id: int
    format_id: int
    set_name: str
    
    class Config:
        from_attributes = True


class FormatBase(BaseModel):
    """Base format schema"""
    name: str = Field(..., max_length=100)
    description: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None


class FormatResponse(FormatBase):
    """Schema for format response"""
    id: int
    created_at: datetime
    updated_at: datetime
    format_sets: list[FormatSetResponse] = []
    
    class Config:
        from_attributes = True
