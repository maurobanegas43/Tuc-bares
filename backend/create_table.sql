-- ============================================
-- CREA ESTA TABLA EN TU SUPABASE DASHBOARD
-- Ve a: https://supabase.com/dashboard
-- Selecciona tu proyecto → SQL Editor
-- ============================================

-- Crear tabla places
CREATE TABLE IF NOT EXISTS places (
  id BIGSERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  address TEXT NOT NULL,
  category TEXT NOT NULL,
  rating REAL,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Habilitar RLS (opcional para desarrollo)
ALTER TABLE places ENABLE ROW LEVEL SECURITY;

-- Policy para lectura pública (ajusta según necesidad)
CREATE POLICY "Allow public read" ON places
  FOR SELECT USING (true);

-- Policy para inserción (solo desde el backend)
CREATE POLICY "Allow service insert" ON places
  FOR INSERT WITH CHECK (true);

-- Policy para删除 (solo desde el backend)
CREATE POLICY "Allow service delete" ON places
  FOR DELETE USING (true);