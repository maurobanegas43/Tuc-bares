import httpx
from api.config.settings import settings
from api.utils.logger import log_info, log_error
from typing import List, Dict, Any, Optional


class GooglePlacesService:
    """Servicio para interactuar con Google Places API (v1)."""
    
    BASE_URL = "https://places.googleapis.com/v1"
    
    # Coordenadas fijas de San Miguel de Tucumán
    TUCUMAN_LAT = -26.817
    TUCUMAN_LNG = -65.2566
    TUCUMAN_RADIUS = 50000  # 50km - máximo permitido por Google Places API  
    
    def __init__(self):
        self.api_key = settings.google_places_api_key
    
    def search_nearby(
        self,
        types: List[str] = None,
        limit: int = 100,
        radius: int = None
    ) -> List[Dict[str, Any]]:
        """
        Busca lugares cercanos usando Google Places API v1.
        
        Args:
            types: Lista de tipos de lugar (default: restaurant, bar, cafe)
            limit: Límite de resultados
            radius: Radio en metros (opcional, usa TUCUMAN_RADIUS por defecto)
        """
        # Usar radio personalizado o el default
        search_radius = radius if radius else self.TUCUMAN_RADIUS
        if not self.api_key:
            log_error("Google Places API key no configurada")
            return []
        
        if types is None:
            types = ["restaurant", "bar", "cafe"]
        
        all_results = []
        
        try:
            # Request a la API v1
            headers = {
                "Content-Type": "application/json",
                "X-Goog-Api-Key": self.api_key,
                "X-Goog-FieldMask": "places.displayName,places.formattedAddress,places.rating,places.primaryType"
            }
            
            # Pagination con hasta 3 páginas
            for page in range(3):
                max_results = min(20, limit - len(all_results))
                if max_results <= 0:
                    break
                
                data = {
                    "includedTypes": types,
                    "maxResultCount": max_results,
                    "locationRestriction": {
                        "circle": {
                            "center": {
                                "latitude": self.TUCUMAN_LAT,
                                "longitude": self.TUCUMAN_LNG
                            },
                            "radius": search_radius
                        }
                    }
                }
                
                response = httpx.post(
                    f"{self.BASE_URL}/places:searchNearby",
                    headers=headers,
                    json=data,
                    timeout=15.0
                )
                
                if response.status_code != 200:
                    log_error(f"Error en API: {response.status_code} - {response.text}")
                    break
                
                result = response.json()
                places = result.get("places", [])
                
                if not places:
                    break
                
                all_results.extend(places)
                
                # Si hay menos de max_results, no hay más páginas
                if len(places) < max_results:
                    break
                    
        except Exception as e:
            log_error(f"Error consultando Google Places: {e}")
        
        return all_results[:limit]
    
    def parse_results(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Procesa resultados de Google Places API v1."""
        places = []
        
        for result in results:
            # Extraer nombre
            display_name = result.get("displayName", {})
            name = display_name.get("text", "") if isinstance(display_name, dict) else ""
            
            # Extraer dirección
            address = result.get("formattedAddress", "")
            
            # Extraer rating
            rating = result.get("rating")
            
            # Extraer tipo primario
            primary_type = result.get("primaryType", "")
            
            # Clasificar categoría
            category = self._classify_category(primary_type)
            
            place = {
                "name": name,
                "address": address,
                "category": category,
                "rating": rating
            }
            
            if place["name"]:
                places.append(place)
        
        return places
    
    def _classify_category(self, primary_type: str) -> str:
        """Clasifica la categoría basándose en el tipo primario."""
        if not primary_type:
            return "otro"
        
        type_lower = primary_type.lower()
        
        if "bar" in type_lower:
            return "bar"
        elif "cafe" in type_lower or "coffee" in type_lower:
            return "café"
        elif "restaurant" in type_lower:
            return "restaurante"
        else:
            return "otro"