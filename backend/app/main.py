from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config.settings import settings
from app.routes.places_routes import router as places_router
from app.routes.chat_routes import router as chat_router
from app.utils.logger import log_info


# Crear app
app = FastAPI(
    title="Tuc-Bares API",
    description="API para obtener bares y restaurantes de Tucumán",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rutas
app.include_router(places_router)
app.include_router(chat_router)


@app.get("/")
async def root():
    """Endpoint raíz."""
    return {"message": "Tuc-Bares API", "status": "running"}


@app.get("/health")
async def health():
    """Health check."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    
    log_info(f"Iniciando servidor en {settings.app_host}:{settings.app_port}")
    
    uvicorn.run(
        "app.main:app",
        host=settings.app_host,
        port=settings.app_port,
        reload=True
    )