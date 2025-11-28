-- Migration: recrear tabla canchas para añadir FOREIGN KEY(usuario_id) y columna direccion
PRAGMA foreign_keys=off;
BEGIN TRANSACTION;

-- Crear nueva tabla con la estructura deseada
CREATE TABLE IF NOT EXISTS canchas_new (
    id_cancha INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    precio TEXT DEFAULT NULL,
    descripcion TEXT DEFAULT NULL,
    imagen_url TEXT DEFAULT NULL,
    tiempo_uso INTEGER DEFAULT 0,
    cronometro_inicio DATETIME DEFAULT NULL,
    direccion TEXT DEFAULT NULL,
    usuario_id INTEGER NOT NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

-- Copiar datos de la tabla antigua a la nueva.
-- Usamos COALESCE(usuario_id, admin_id) por compatibilidad con esquemas antiguos que usaban admin_id.
INSERT INTO canchas_new (id_cancha, nombre, precio, descripcion, imagen_url, tiempo_uso, cronometro_inicio, direccion, usuario_id)
SELECT id_cancha, nombre, precio, descripcion, imagen_url, tiempo_uso, cronometro_inicio, NULL as direccion, COALESCE(usuario_id, admin_id)
FROM canchas;

-- Reemplazar la tabla antigua
DROP TABLE canchas;
ALTER TABLE canchas_new RENAME TO canchas;

COMMIT;
PRAGMA foreign_keys=on;
