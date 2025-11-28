-- Migration: renombrar admin_id a usuario_id y añadir columna direccion en canchas
PRAGMA foreign_keys=off;
BEGIN TRANSACTION;

-- Intentar renombrar la columna (requiere SQLite >= 3.25)
ALTER TABLE canchas RENAME COLUMN admin_id TO usuario_id;

-- Añadir columna direccion si no existe
ALTER TABLE canchas ADD COLUMN direccion TEXT DEFAULT NULL;

COMMIT;
PRAGMA foreign_keys=on;
