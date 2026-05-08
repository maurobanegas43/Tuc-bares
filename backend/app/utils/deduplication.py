import unicodedata
import re
from typing import List, Tuple


def normalize_text(text: str) -> str:
    """Normaliza texto para comparación."""
    if not text:
        return ""
    
    # Convertir a minúsculas
    text = text.lower()
    
    # Normalizar unicode (acentos)
    text = unicodedata.normalize("NFD", text)
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    
    # Eliminar caracteres especiales
    text = re.sub(r"[^a-z0-9\s]", "", text)
    
    # Eliminar espacios extra
    text = " ".join(text.split())
    
    return text.strip()


def normalize_address(address: str) -> str:
    """Normaliza dirección para comparación."""
    if not address:
        return ""
    
    # Normalizar texto base
    address = normalize_text(address)
    
    # reemplazar comunes
    replacements = {
        "av ": "avenida ",
        "av. ": "avenida ",
        "calle ": "",
        "n ": " #",
        " no": " #",
    }
    
    for old, new in replacements.items():
        address = address.replace(old, new)
    
    return address.strip()


def check_duplicate(
    new_name: str,
    new_address: str,
    existing: List[Tuple[str, str]],
    threshold: int = 80
) -> bool:
    """Verifica si ya existe un registro similar."""
    from rapidfuzz import fuzz
    
    new_name_norm = normalize_text(new_name)
    new_address_norm = normalize_address(new_address)
    
    for existing_name, existing_address in existing:
        existing_name_norm = normalize_text(existing_name)
        existing_address_norm = normalize_address(existing_address)
        
        # Comparar nombres
        name_ratio = fuzz.ratio(new_name_norm, existing_name_norm)
        
        # Comparar direcciones
        address_ratio = fuzz.ratio(new_address_norm, existing_address_norm)
        
        # Si ambos son muy similares, es duplicado
        if name_ratio >= threshold and address_ratio >= threshold:
            return True
        
        # Si el nombre es igual y la dirección contiene parte
        if name_ratio >= threshold and (
            new_address_norm in existing_address_norm or 
            existing_address_norm in new_address_norm
        ):
            return True
    
    return False