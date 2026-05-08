from datetime import datetime
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field


class Place(BaseModel):
    """Modelo de lugar."""
    id: Optional[int] = None
    name: str
    address: str
    category: str
    rating: Optional[float] = None
    created_at: Optional[datetime] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte a diccionario."""
        return self.model_dump()


class PlaceCreate(BaseModel):
    """Schema para crear lugar."""
    name: str = Field(..., min_length=1, max_length=255)
    address: str = Field(..., min_length=1, max_length=500)
    category: str = Field(..., min_length=1, max_length=100)
    rating: Optional[float] = Field(None, ge=0, le=5)


class PlaceResponse(BaseModel):
    """Schema para respuesta de lugar."""
    id: int
    name: str
    address: str
    category: str
    rating: Optional[float] = None
    created_at: datetime