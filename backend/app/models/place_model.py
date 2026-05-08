from pydantic import BaseModel, Field
from typing import Optional


class PlaceModel(BaseModel):
    """Modelo de datos para la tabla places."""
    id: Optional[int] = None
    name: str = Field(..., min_length=1, max_length=255)
    address: str = Field(..., min_length=1, max_length=500)
    category: str = Field(..., min_length=1, max_length=100)
    rating: Optional[float] = Field(None, ge=0, le=5)
    created_at: Optional[str] = None
    
    class Config:
        from_attributes = True