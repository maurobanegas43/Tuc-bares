from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from api.services.places_service import PlacesService
from api.schemas.place_schema import Place, PlaceCreate, PlaceResponse
from api.utils.logger import log_info, log_error


router = APIRouter(prefix="/places", tags=["places"])
service = PlacesService()


@router.get("", response_model=List[PlaceResponse])
async def get_places(limit: int = Query(10, ge=10, le=50)):
    """
    Obtiene lugares de la base de datos.
    
    - Si hay suficientes registros, los devuelve desde DB
    - Si no, consulta Google Places y guarda los nuevos
    """
    try:
        places = service.get_places(limit=limit)
        return places
    except Exception as e:
        log_error(f"Error obtener lugares: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("", response_model=dict)
async def delete_places():
    """Borra todos los lugares."""
    try:
        count = service.delete_all()
        return {"deleted": count, "message": f"Se borraron {count} lugares"}
    except Exception as e:
        log_error(f"Error borrar lugares: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{place_id}", response_model=dict)
async def delete_place(place_id: int):
    """Borra un lugar por ID."""
    try:
        deleted = service.delete_one(place_id)
        if deleted:
            return {"deleted": 1, "message": f"Lugar {place_id} eliminado"}
        raise HTTPException(status_code=404, detail="Lugar no encontrado")
    except HTTPException:
        raise
    except Exception as e:
        log_error(f"Error borrar lugar: {e}")
        raise HTTPException(status_code=500, detail=str(e))