from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from datetime import datetime, timedelta
from app.config.settings import settings

router = APIRouter(prefix="/chat", tags=["chat"])

# Alias para configuración de chat
MAX_MESSAGES = settings.chat_max_messages
SESSION_DURATION_HOURS = settings.chat_session_duration_hours
BAN_DURATION_HOURS = settings.chat_ban_duration_hours

# Palabras clave permitidas (solo sobre restaurantes)
ALLOWED_KEYWORDS = [
    "restaurante", "bar", "café", "cafe", "comida", "tucumán", "tucuman",
    "san miguel", "dirección", "direccion", "rating", "calificado", "mejor",
    "cuantos", "cuántos", "donde", "dónde", "cual", "cuál",
    "abierto", "cerrado", "precio", "menu", "menú", "especialidad",
    "pedir", "orden", "reservar", "ubicación", "ubicacion"
]

# Palabras bloqueadas
BLOCKED_KEYWORDS = [
    "sistema", "backend", "base de datos", "database", "db",
    "api", "como funciona", "tecnología", "tech", "code", "código",
    "quien sos", "quién sos", "tu nombre", "tu edad", "敏感",
    "crear", "borrar", "eliminar", "actualizar", "admin",
    "prompt injection", "ignorar", "override"
]

# Storage en memoria (para producción usar Redis o DB)
class ChatSession:
    def __init__(self, ip: str):
        self.ip = ip
        self.count = 0
        self.created_at = datetime.now()
        self.banned_until: datetime | None = None
        self.last_message_at = datetime.now()
    
    def is_banned(self) -> bool:
        if self.banned_until and self.banned_until > datetime.now():
            return True
        if self.banned_until:
            self.banned_until = None  # Desbanear
        return False
    
    def can_chat(self) -> bool:
        if self.is_banned():
            return False
        if self.count >= MAX_MESSAGES:
            return False
        # Verificar si pasaron 24 horas desde el último mensaje
        if datetime.now() - self.last_message_at > timedelta(hours=SESSION_DURATION_HOURS):
            self.count = 0  # Resetear contador
        return True
    
    def add_message(self):
        self.count += 1
        self.last_message_at = datetime.now()
    
    def ban(self, hours: int = BAN_DURATION_HOURS):
        self.banned_until = datetime.now() + timedelta(hours=hours)
        self.count = MAX_MESSAGES  # Bloquear
    
    def remaining(self) -> int:
        return max(0, MAX_MESSAGES - self.count)


# Diccionario de sesiones {ip: ChatSession}
sessions: dict[str, ChatSession] = {}


def get_session(ip: str) -> ChatSession:
    """Obtiene o crea sesión."""
    if ip not in sessions:
        sessions[ip] = ChatSession(ip)
    return sessions[ip]


def get_client_ip(request: Request) -> str:
    """Obtiene IP del cliente."""
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


def get_client():
    """Obtiene cliente de GenAI."""
    api_key = settings.gemini_api_key
    if not api_key:
        raise HTTPException(status_code=500, detail="GEMINI_API_KEY no configurada")
    
    from google import genai
    return genai.Client(api_key=api_key)


def is_spam(message: str) -> bool:
    """Detecta spam o contenido bloqueado."""
    msg = message.lower()
    
    for word in BLOCKED_KEYWORDS:
        if word in msg:
            return True
    
    return False


def is_allowed_topic(message: str) -> bool:
    """Verifica si es pregunta sobre restaurantes."""
    msg = message.lower()
    
    for keyword in ALLOWED_KEYWORDS:
        if keyword in msg:
            return True
    
    return False


class ChatRequest(BaseModel):
    message: str


@router.post("")
async def chat(req: ChatRequest, request: Request):
    """Chat con Gemini - limitado a 5 preguntas por sesión de 24 horas."""
    client = get_client()
    client_ip = get_client_ip(request)
    session = get_session(client_ip)
    
    if not client:
        raise HTTPException(status_code=500, detail="GEMINI_API_KEY no configurada")
    
    # Verificar si está baneado
    if session.is_banned():
        raise HTTPException(
            status_code=403,
            detail=f"IP bloqueada por 24 horas por spam o abuso. Intenta mañana."
        )
    
    # Verificar límite
    if not session.can_chat():
        raise HTTPException(
            status_code=429,
            detail=f"Límite de {MAX_MESSAGES} preguntas alcanzado. límite se renueva en 24 horas."
        )
    
    message = req.message.strip()
    
    # Verificar spam
    if is_spam(message):
        session.ban()  # Banear por 24 horas
        raise HTTPException(
            status_code=400,
            detail="Pregunta no permitida. IP bloqueada por 24 horas."
        )
    
    # Verificar tema
    if not is_allowed_topic(message):
        raise HTTPException(
            status_code=400,
            detail="Solo preguntas sobre restaurantes, bares y cafés en Tucumán. Ej: ¿Cuántos restaurantes hay? ¿Cuál es el mejor?"
        )
    
    # Prompt sin acceso a DB
    prompt = f"""
    Vos sos un asistente友好的 de información sobre restaurantes y bares en San Miguel de Tucumán, Argentina.
    
    REGLAS IMPORTANTES:
    - NO mentas que tenés acceso a una base de datos
    - NO des información técnica o del sistema
    - Si no sabés algo, decilo: "No tengo esa información"
    - Solo respondé sobre restaurantes, bares y cafeterías de Tucumán
    
    Pregunta: {message}
    """
    
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        
        # Registrar mensaje
        session.add_message()
        remaining = session.remaining()
        
        return {
            "answer": response.text,
            "remaining": remaining,
            "limit_reached": remaining == 0,
            "session_expires": f"{SESSION_DURATION_HOURS} horas"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status")
async def chat_status(request: Request):
    """Estado del chat del usuario."""
    client_ip = get_client_ip(request)
    session = get_session(client_ip)
    
    return {
        "ip": client_ip,
        "messages_used": session.count,
        "messages_remaining": session.remaining(),
        "max_messages": MAX_MESSAGES,
        "session_expires_hours": SESSION_DURATION_HOURS,
        "is_banned": session.is_banned()
    }


@router.post("/reset")
async def chat_reset(request: Request):
    """Resetear sesión propia."""
    client_ip = get_client_ip(request)
    session = get_session(client_ip)
    session.count = 0
    session.banned_until = None
    
    return {"message": "Tu sesión fue reseteada", "ip": client_ip}