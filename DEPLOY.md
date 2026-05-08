# Guía de Deploy en Render

## Problemas corregidos

1. ✅ Rutas hardcodeadas eliminadas
2. ✅ Script de inicio corregido
3. ✅ Archivo render.yaml creado
4. ✅ Archivos .env.example agregados

## Pasos para deployar

### Opción 1: Usando render.yaml (Recomendado)

1. **Sube tu código a GitHub**
   ```bash
   git add .
   git commit -m "Fix: Optimización para build en Render"
   git push origin main
   ```

2. **En Render Dashboard**
   - Ve a https://dashboard.render.com
   - Click en "New" → "Blueprint"
   - Conecta tu repositorio de GitHub
   - Render detectará automáticamente el `render.yaml`

3. **Configura las variables de entorno**
   En cada servicio, agrega:
   
   **Backend:**
   - `SUPABASE_URL`: https://zzukuvuieulyqfneygav.supabase.co
   - `SUPABASE_KEY_ANON`: tu_anon_key
   - `SUPABASE_KEY_ROLE`: tu_service_role_key
   - `GOOGLE_PLACES_API_KEY`: tu_google_api_key
   - `GEMINI_API_KEY`: tu_gemini_api_key
   
   **Frontend:**
   - `VITE_API_URL`: https://tuc-bares-api.onrender.com (URL de tu backend)

### Optimizaciones aplicadas

- ✅ Versiones fijas de dependencias para builds reproducibles
- ✅ Python 3.11.9 (más estable que 3.14 para producción)
- ✅ Build command optimizado
- ✅ Frontend configurado como static site (más eficiente)
- ✅ Archivos runtime.txt y .python-version agregados

### Opción 2: Deploy manual (Si Blueprint no funciona)

Si el deploy con Blueprint tiene problemas, usa deploy manual:

#### Backend:
1. En Render Dashboard: New → Web Service
2. Conecta tu repositorio
3. Configuración:
   - **Name**: tuc-bares-api
   - **Root Directory**: backend
   - **Environment**: Python 3
   - **Build Command**: `pip install --upgrade pip && pip install -r requirements.txt`
   - **Start Command**: `uvicorn api.main:app --host 0.0.0.0 --port $PORT`
   - **Plan**: Free

4. Environment Variables (en el dashboard):
   ```
   PYTHON_VERSION=3.11.9
   SUPABASE_URL=https://zzukuvuieulyqfneygav.supabase.co
   SUPABASE_KEY_ANON=tu_anon_key
   SUPABASE_KEY_ROLE=tu_service_role_key
   GOOGLE_PLACES_API_KEY=tu_google_api_key
   GEMINI_API_KEY=tu_gemini_api_key
   APP_HOST=0.0.0.0
   APP_PORT=8000
   ```

#### Frontend:
1. New → Static Site
2. Conecta tu repo
3. Configuración:
   - **Name**: tuc-bares-frontend
   - **Root Directory**: frontend
   - **Build Command**: `npm install && npm run build`
   - **Publish Directory**: `dist`
   - **Plan**: Free

4. Environment Variables:
   ```
   VITE_API_URL=https://tuc-bares-api.onrender.com
   ```
   (Reemplaza con la URL real de tu backend una vez deployado)

## Verificación

Después del deploy:

1. **Backend**: Visita `https://tu-backend.onrender.com/health`
   - Debe responder: `{"status": "healthy"}`

2. **Frontend**: Visita tu URL del frontend
   - Debe cargar la aplicación correctamente

## Notas importantes

- ⚠️ **NO subas el archivo .env a GitHub** (ya está en .gitignore)
- ⚠️ Las variables de entorno deben configurarse en el dashboard de Render
- ⚠️ El primer deploy puede tardar 5-10 minutos
- ⚠️ Render free tier pone los servicios en sleep después de inactividad

## Troubleshooting

### Error: "Module not found"
- Verifica que el start command sea: `cd backend && uvicorn api.main:app --host 0.0.0.0 --port $PORT`

### Error: "Environment variables not found"
- Verifica que todas las variables estén configuradas en Render Dashboard

### Frontend no conecta con backend
- Verifica que `VITE_API_URL` apunte a la URL correcta del backend
- Asegúrate de hacer rebuild del frontend después de cambiar variables

### CORS errors
- El backend ya tiene CORS configurado para permitir todos los orígenes
- Si persiste, verifica que la URL del backend sea correcta
