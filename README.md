# 🍻 Tuc-Bares

> Descubrí los mejores bares y restaurantes de San Miguel de Tucumán

![React](https://img.shields.io/badge/React-19.2.5-61DAFB?logo=react)
![TypeScript](https://img.shields.io/badge/TypeScript-6.0-blue?logo=typescript)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-009688?logo=fastapi)
![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python)
![Supabase](https://img.shields.io/badge/Supabase-2.9.0-3ECF8E?logo=supabase)
![License](https://img.shields.io/badge/License-MIT-green)

## 📋 Descripción

Aplicación web para explorar bares y restaurantes de Tucumán. Permite buscar lugares, ver detalles, cargarlos desde Google Places y chatear con un asistente IA para recomendaciones.

---

## 🏗️ Arquitectura

```
Tuc-bares/
├── backend/              # API FastAPI
│   ├── api/
│   │   ├── config/       # Configuración (pydantic-settings)
│   │   ├── database/     # Cliente Supabase
│   │   ├── models/       # Modelos Pydantic
│   │   ├── repositories/ # Capa de datos (CRUD Supabase)
│   │   ├── routes/       # Endpoints HTTP
│   │   ├── schemas/      # Schemas de request/response
│   │   ├── services/     # Lógica de negocio
│   │   └── utils/        # Deduplicación, logging
│   ├── requirements.txt
│   └── render.yaml       # Deploy con Blueprint
│
└── frontend/            # App React + Vite
    ├── src/
    │   ├── App.tsx       # Componente principal
    │   ├── api.ts        # Cliente API
    │   └── types.ts      # Tipos TypeScript
    └── dist/             # Build de producción
```

---

## ⚙️ Stack Tecnológico

### Backend
| Dependencia | Versión |
|------------|---------|
| Python | 3.11.9 |
| FastAPI | 0.115.0 |
| Uvicorn | 0.30.6 |
| Pydantic | 2.10.0 |
| Supabase | 2.9.0 |
| google-genai | 0.8.0 |
| httpx | 0.27.0 |
| rapidfuzz | 3.6.1 |

### Frontend
| Dependencia | Versión |
|------------|---------|
| React | 19.2.5 |
| Vite | 8.0.10 |
| TypeScript | ~6.0.2 |
| DM Sans + Fraunces | — |

### Servicios externos
- **Base de datos:** Supabase (PostgreSQL)
- **Datos de lugares:** Google Places API v1
- **Chat IA:** Google Gemini 2.5 Flash
- **Hosting:** Render (backend + frontend)

---

## 🚀 Setup local

### Requisitos
- Python 3.11+
- Node.js 18+
- Cuenta de Supabase
- Clave de Google Places API
- Clave de Google Gemini API

### Backend

```bash
cd backend

# Crear entorno virtual
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus claves

# Crear tabla en Supabase
psql < create_table.sql
# O ejecutar el SQL desde el dashboard de Supabase

# Correr servidor
uvicorn api.main:app --reload
```

### Frontend

```bash
cd frontend

npm install

# Configurar variable de entorno
cp .env.example .env
# Editar .env: VITE_API_URL=http://localhost:8000

npm run dev
```

---

## 🔑 Variables de entorno

### Backend (`backend/.env`)
```env
SUPABASE_URL=https://tu-proyecto.supabase.co
SUPABASE_KEY_ANON=tu_anon_key
SUPABASE_KEY_ROLE=tu_service_role_key
GOOGLE_PLACES_API_KEY=tu_google_places_key
GEMINI_API_KEY=tu_gemini_key
```

### Frontend (`frontend/.env`)
```env
VITE_API_URL=http://localhost:8000
```

---

## 🌐 API Endpoints

### Lugares

| Método | Ruta | Descripción |
|--------|------|-------------|
| `GET` | `/` | Info de la API |
| `GET` | `/health` | Health check |
| `GET` | `/places` | Lista de lugares (query: `?limit=10`) |
| `DELETE` | `/places` | Borrar todos los lugares |
| `DELETE` | `/places/{id}` | Borrar un lugar |

### Chat

| Método | Ruta | Descripción |
|--------|------|-------------|
| `POST` | `/chat` | Chat con Gemini (body: `{"message": "..."}`) |
| `GET` | `/chat/status` | Estado de la sesión |
| `POST` | `/chat/reset` | Resetear sesión propia |

---

## 🚢 Deploy

### Render (recomendado)

1. Subí el código a GitHub
2. Andá a [dashboard.render.com](https://dashboard.render.com) → **New** → **Blueprint**
3. Conectá el repo `maurobanegas43/Tuc-bares`
4. Render detectará el `render.yaml` y creará ambos servicios
5. Configurá las variables de entorno en cada servicio:

**Backend:**
- `SUPABASE_URL`
- `SUPABASE_KEY_ANON`
- `SUPABASE_KEY_ROLE`
- `GOOGLE_PLACES_API_KEY`
- `GEMINI_API_KEY`

**Frontend:**
- `VITE_API_URL` → URL del backend (ej: `https://tu-backend.onrender.com`)

> ⚠️ El primer deploy puede tardar 5-10 minutos. Render free tier pone los servicios en sleep después de inactividad.

### Vercel (frontend)

1. Importá el repo en [vercel.com](https://vercel.com)
2. Configurá:
   - **Build Command:** `cd frontend && npm install && npm run build`
   - **Output Directory:** `frontend/dist`
3. Agregá variable:
   - `VITE_API_URL` → URL del backend

---

## 🔒 Seguridad

- Las API keys y credenciales se manejan exclusivamente por variables de entorno
- `.env` está excluido de Git (`.gitignore`)
- CORS configurado para producción
- Rate limiting en el chat (5 mensajes por sesión de 24h)
- Filtro anti-spam y palabras bloqueadas

---

## 📁 Archivos importantes

| Archivo | Descripción |
|---------|-------------|
| `backend/create_table.sql` | Schema SQL para Supabase |
| `backend/render.yaml` | Configuración de deploy (Blueprint) |
| `DEPLOY.md` | Guía detallada de deploy |
| `frontend/vite.config.ts` | Configuración de Vite |
| `vercel.json` | Configuración de Vercel |

---

## 🛠️ Desarrollo futuros

- [ ] Tests (pytest + Vitest)
- [ ] Persistencia de sesiones de chat en Supabase (Redis)
- [ ] Autenticación de usuarios
- [ ] Reseñas y favoritos
- [ ] Despliegue de frontend en Render con el Blueprint

---

## 📝 Licencia

MIT
