from typing import List, Optional
from api.database.connection import get_supabase_client


class PlacesRepository:
    """Repositorio para lugares usando Supabase."""
    
    def __init__(self):
        self.client = get_supabase_client()
        self.table = "places"
    
    def get_all(self, limit: Optional[int] = None) -> List[dict]:
        """Obtiene todos los lugares."""
        query = self.client.table(self.table).select("*")
        
        if limit:
            query = query.limit(limit)
        
        response = query.execute()
        return response.data or []
    
    def count(self) -> int:
        """Cuenta cuántos lugares existen."""
        response = self.client.table(self.table).select("*", count="exact").limit(1).execute()
        return response.count or 0
    
    def get_all_names_addresses(self) -> List[tuple]:
        """Obtiene todos los nombres y direcciones."""
        response = self.client.table(self.table).select("name", "address").execute()
        return [(p.get("name"), p.get("address")) for p in response.data if p.get("name")]
    
    def insert(self, place: dict) -> dict:
        """Inserta un lugar."""
        response = self.client.table(self.table).insert(place).execute()
        return response.data[0] if response.data else place
    
    def insert_many(self, places: List[dict]) -> List[dict]:
        """Inserta varios lugares."""
        if not places:
            return []
        
        response = self.client.table(self.table).insert(places).execute()
        return response.data or []
    
    def delete_all(self) -> int:
        """Borra todos los lugares."""
        count = self.count()
        if count > 0:
            self.client.table(self.table).delete().neq("id", 0).execute()
        return count
    
    def delete_one(self, place_id: int) -> bool:
        """Borra un lugar por ID."""
        response = self.client.table(self.table).delete().eq("id", place_id).execute()
        return len(response.data) > 0