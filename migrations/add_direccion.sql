-- Migration: añadir columna 'direccion' a la tabla usuarios

ALTER TABLE usuarios ADD COLUMN direccion TEXT DEFAULT NULL;
