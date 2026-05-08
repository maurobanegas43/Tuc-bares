from app.repositories.places_repository import PlacesRepository
from app.services.google_places_service import GooglePlacesService
from app.utils.deduplication import check_duplicate
from app.utils.logger import log_info, log_error
from typing import List, Dict, Any


class PlacesService:
    """Servicio principal de lugares."""
    
    def __init__(self):
        self.repository = PlacesRepository()
        self.google_service = GooglePlacesService()
    
    def get_places(self, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Obtiene lugares.
        
        Si hay suficientes en DB, los devuelve.
        Si no, consulta Google Places y guarda los nuevos.
        """
        # Verificar cuántos hay en DB
        current_count = self.repository.count()
        
        log_info(f"Lugares en DB: {current_count}, solicitados: {limit}")
        
        # Si hay suficientes, devolver
        if current_count >= limit:
            places = self.repository.get_all(limit=limit)
            return places
        
        # Si no hay suficientes, consultar API
        needed = limit - current_count
        log_info(f"Consultando API para obtener {needed} lugares nuevos")
        
        # Consultar Google Places
        results = self.google_service.search_nearby(limit=needed + 10)
        
        if not results:
            # Devolver lo que hay
            places = self.repository.get_all(limit=limit)
            return places
        
        # Procesar y filtrar duplicados
        parsed_results = self.google_service.parse_results(results)
        
        existing = self.repository.get_all_names_addresses()
        
        new_places = []
        for place in parsed_results:
            if check_duplicate(place["name"], place["address"], existing):
                continue
            
            new_places.append(place)
            existing.append((place["name"], place["address"]))
        
        log_info(f"Lugares nuevos (sin duplicados): {len(new_places)}")
        
        # Si no hay lugares nuevos (todos duplicados), buscar con radio mayor (50km - máximo API)
        if len(new_places) == 0:
            log_info("Todos duplicados. Buscando con radio de 50km...")
            results_extended = self.google_service.search_nearby(limit=needed + 20, radius=50000)
            
            if results_extended:
                parsed_extended = self.google_service.parse_results(results_extended)
                
                for place in parsed_extended:
                    if check_duplicate(place["name"], place["address"], existing):
                        continue
                    
                    new_places.append(place)
                    existing.append((place["name"], place["address"]))
                
                log_info(f"Lugares nuevos con radio 100km: {len(new_places)}")
        
        # Guardar solo los nuevos
        if new_places:
            self.repository.insert_many(new_places)
        
        # Devolver todos
        all_places = self.repository.get_all(limit=limit)
        return all_places
    
    def delete_all(self) -> int:
        """Borra todos los lugares."""
        count = self.repository.count()
        
        if count > 0:
            self.repository.delete_all()
            log_info(f"Borrados {count} lugares")
        
        return count
    
    def delete_one(self, place_id: int) -> bool:
        """Borra un lugar por ID."""
        return self.repository.delete_one(place_id)