# CONTEXTO DEL PROYECTO

El sistema debe obtener y mostrar  restaurantes o bares de San Miguel de Tucumán utilizando Google Places API.

# STACK TECNOLÓGICO

## Frontend
- React

## Backend
- Python
- FastAPI

## Base de datos
- Supabase (PostgreSQL)

## API externa
- Google Places API
- Google geminis modelo 2.5 flash 

# OBJETIVO DEL SISTEMA

Construir un MVP simple que:

1. Consulte Google Places API.
2. Obtenga restaurantes/bares.
3. Procese y filtre datos.
4. Guarde únicamente nuevos registros.
5. Consulte los datos desde la base de datos.
6. Evite solicitudes innecesarias a la API.
7. Permita aumentar progresivamente la cantidad de resultados mostrados.
8. Limitar la cantidad de peticiones a la api de google place , asi como tambien a la geminis manteniendo los costos en 0 

# DATOS A EXTRAER

Extraer únicamente:

- nombre
- dirección
- categoría
- rating

# FLUJO PRINCIPAL

## Primera carga

Cuando el usuario entra por primera vez:

1. El frontend solicita datos al backend.
2. El backend consulta la base de datos.
3. Si no existen registros:
   - consultar Google Places API
   - procesar resultados
   - guardar en DB
   - devolver datos al frontend

## Siguientes cargas

Si ya existen datos:

- GET obtiene datos únicamente desde la DB
- NO consultar nuevamente la API

## Solicitud de más resultados

Ejemplo:

- inicialmente mostrar 10
- luego 20
- luego 30
- hasta 50

Cuando el usuario solicita más resultados:

1. backend revisa cantidad actual en DB
2. si ya existen suficientes:
   - devolver desde DB
3. si faltan registros:
   - consultar API
   - comparar nuevos registros
   - guardar solo los que no existan
   - devolver resultados actualizados

# REGLAS IMPORTANTES

## POST

POST solamente se usa internamente cuando llegan datos desde Google Places API.

NO existe creación manual desde frontend.

## GET

GET siempre obtiene datos desde la DB.

## DELETE

Debe existir un botón para:

- borrar todos los datos almacenados

# MANEJO DE DUPLICADOS

Antes de guardar nuevos datos:

- leer registros existentes
- comparar nombres y direcciones

Guardar únicamente registros nuevos.

# MANEJO DE RATE LIMIT

Evitar solicitudes innecesarias a Google Places API.

La API SOLO debe consultarse cuando:

- la DB está vacía
- el usuario solicita más lugares y no existen suficientes registros guardados

# ARQUITECTURA BACKEND

Arquitectura simple por capas.

# ESTRUCTURA DEL BACKEND

backend/
│
├── app/
│   ├── main.py
│   │
│   ├── routes/
│   │   └── places_routes.py
│   │
│   ├── services/
│   │   ├── places_service.py
│   │   └── google_places_service.py
│   │
│   ├── repositories/
│   │   └── places_repository.py
│   │
│   ├── models/
│   │   └── place_model.py
│   │
│   ├── schemas/
│   │   └── place_schema.py
│   │
│   ├── database/
│   │   └── connection.py
│   │
│   ├── utils/
│   │   ├── deduplication.py
│   │   └── logger.py
│   │
│   └── config/
│       └── settings.py
│
├── requirements.txt
└── .env

# RESPONSABILIDAD DE CADA CAPA

## routes

Define endpoints FastAPI.

Ejemplo:
- GET /places
- DELETE /places

## services

Contiene lógica de negocio.

Ejemplo:
- decidir cuándo consultar API
- procesar datos
- validar duplicados

## repositories

Acceso a base de datos.

Ejemplo:
- guardar registros
- obtener registros
- borrar registros

## models

Modelo de tabla DB.

## schemas

Validaciones Pydantic.

## utils

Funciones auxiliares:
- logs
- deduplicación

# ESTRATEGIA SIMPLE DE DUPLICADOS

Comparar:

- nombre normalizado
- dirección normalizada

Ejemplo:

"Bar Irlanda"
"Irlanda Bar"

Puede utilizarse:

- rapidfuzz

NO usar modelos pesados.

# IA PARA LA PRUEBA

La IA debe ser simple y práctica.

## OPCIÓN RECOMENDADA

Usar clasificación basada en reglas.

Ejemplo:

Si categoría contiene:
- "cafe" → café
- "bar" → bar
- "restaurant" → restaurante

Esto ya cuenta como uso práctico de IA/simple procesamiento inteligente para un MVP.

## OPCIÓN MEJOR

Usar embeddings livianos.

Modelo recomendado:

- sentence-transformers/all-MiniLM-L6-v2

Uso:
- detectar similitud entre nombres
- mejorar deduplicación

Ventajas:
- liviano
- rápido
- fácil de integrar
- suficiente para esta prueba

NO usar modelos grandes ni LLMs complejos.

# BASE DE DATOS

Tabla: places

Campos:

- id
- name
- address
- category
- rating
- created_at

# ENDPOINTS

## GET /places?limit=10

Obtiene lugares desde DB.

## DELETE /places

Borra todos los registros.

# LÓGICA DE PAGINACIÓN

Frontend solicita:

- limit=10
- limit=20
- limit=30

Backend:

1. revisa cantidad existente
2. consulta API solo si necesita más datos
3. guarda únicamente nuevos registros

# FRONTEND

## FUNCIONALIDADES

- listado de restaurantes
- botón "cargar más"
- botón borrar datos
- loading states
- manejo básico de errores

# OBJETIVO DEL AGENTE

Actuar como un ingeniero backend senior enfocado en:

- FastAPI
- arquitectura por capas simple
- manejo eficiente de APIs
- deduplicación
- procesamiento de datos
- MVPs limpios y mantenibles

El agente debe:

- evitar sobreingeniería
- mantener código simple
- priorizar claridad
- modularizar correctamente
- justificar decisiones técnicas
- reutilizar lógica
- minimizar llamadas a APIs externas
