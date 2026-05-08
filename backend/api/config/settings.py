from pydantic_settings import BaseSettings
from typing import Optional
from dotenv import load_dotenv
import os

# Cargar .env desde la ruta relativa
load_dotenv()


class Settings(BaseSettings):
    # Supabase
    supabase_url: str = ""
    supabase_key_anon: str = ""
    supabase_key_role: str = ""
    
    # Google Places
    google_places_api_key: str = ""
    
    # Google Gemini
    gemini_api_key: str = ""
    
    # Chat
    chat_max_messages: int = 5
    chat_session_duration_hours: int = 24
    chat_ban_duration_hours: int = 24
    
    # App
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


settings = Settings()