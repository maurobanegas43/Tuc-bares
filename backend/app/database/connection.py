import os
from supabase import create_client
from dotenv import load_dotenv

# Cargar desde la ruta correcta
load_dotenv("/home/mauro/Documentos/Tuc-bares/backend/.env")

# Cache del cliente
_client = None


def get_supabase_client():
    """Obtiene cliente de Supabase (service role para backend)."""
    global _client
    
    if _client:
        return _client
    
    url = os.getenv("SUPABASE_URL", "")
    key = os.getenv("SUPABASE_KEY_ROLE", "")
    
    if not url or not key:
        raise ValueError("SUPABASE_URL y SUPABASE_KEY_ROLE deben estar configurados")
    
    _client = create_client(url, key)
    return _client