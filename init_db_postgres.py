"""
Script para crear el esquema de la base de datos en PostgreSQL
Este script se ejecuta automáticamente en Railway al hacer deploy
"""
import os
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash

# Cargar variables de entorno si existen (para desarrollo local)
load_dotenv()

def create_schema():
    """Crea todas las tablas en PostgreSQL"""
    
    # Obtener URL de la base de datos
    database_url = os.getenv('DATABASE_URL')
    
    if not database_url:
        print("❌ Error: DATABASE_URL no está configurada")
        print("💡 Para desarrollo local, usa SQLite con init_db.py")
        return False
        
    # Limpiar espacios en blanco o saltos de línea
    database_url = database_url.strip()
    
    # Convertir formato si es necesario
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    
    try:
        # Conectar a PostgreSQL
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        
        print("🔗 Conectado a PostgreSQL")
        print("📋 Creando tablas...")
        
        # SQL para crear las tablas (adaptado para PostgreSQL)
        schema_sql = """
        -- Tabla: usuarios
        CREATE TABLE IF NOT EXISTS usuarios (
            id SERIAL PRIMARY KEY,
            nombre VARCHAR(255) NOT NULL,
            correo VARCHAR(255) NOT NULL UNIQUE,
            edad INTEGER NOT NULL,
            contraseña VARCHAR(255) NOT NULL,
            direccion TEXT DEFAULT NULL,
            rol VARCHAR(50) NOT NULL DEFAULT 'usuario'
        );
        
        -- Tabla: canchas
        CREATE TABLE IF NOT EXISTS canchas (
            id_cancha SERIAL PRIMARY KEY,
            nombre VARCHAR(255) NOT NULL,
            precio VARCHAR(50) DEFAULT NULL,
            descripcion TEXT DEFAULT NULL,
            imagen_url TEXT DEFAULT NULL,
            tiempo_uso INTEGER DEFAULT 0,
            cronometro_inicio TIMESTAMP DEFAULT NULL,
            direccion TEXT DEFAULT NULL,
            usuario_id INTEGER NOT NULL,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
        );
        
        -- Tabla: favoritos
        CREATE TABLE IF NOT EXISTS favoritos (
            id_favorito SERIAL PRIMARY KEY,
            id_usuario INTEGER NOT NULL,
            cancha VARCHAR(255) NOT NULL,
            fecha_agregado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (id_usuario) REFERENCES usuarios(id) ON DELETE CASCADE
        );
        
        -- Tabla: horarios_canchas
        CREATE TABLE IF NOT EXISTS horarios_canchas (
            id_horario SERIAL PRIMARY KEY,
            id_cancha INTEGER NOT NULL,
            hora_inicio TIME NOT NULL,
            hora_fin TIME NOT NULL,
            disponible BOOLEAN DEFAULT TRUE,
            FOREIGN KEY (id_cancha) REFERENCES canchas(id_cancha) ON DELETE CASCADE
        );
        
        -- Tabla: reservas
        CREATE TABLE IF NOT EXISTS reservas (
            id_reserva SERIAL PRIMARY KEY,
            id_usuario INTEGER NOT NULL,
            cancha VARCHAR(255) NOT NULL,
            horario VARCHAR(100) NOT NULL,
            fecha DATE NOT NULL,
            numero VARCHAR(50),
            mensaje TEXT,
            FOREIGN KEY (id_usuario) REFERENCES usuarios(id) ON DELETE CASCADE
        );
        
        -- Índices para mejorar rendimiento
        CREATE INDEX IF NOT EXISTS idx_usuarios_correo ON usuarios(correo);
        CREATE INDEX IF NOT EXISTS idx_usuarios_rol ON usuarios(rol);
        CREATE INDEX IF NOT EXISTS idx_canchas_usuario ON canchas(usuario_id);
        CREATE INDEX IF NOT EXISTS idx_favoritos_usuario ON favoritos(id_usuario);
        CREATE INDEX IF NOT EXISTS idx_reservas_usuario ON reservas(id_usuario);
        CREATE INDEX IF NOT EXISTS idx_reservas_fecha ON reservas(fecha);
        """
        
        # Ejecutar el script
        cursor.execute(schema_sql)
        conn.commit()
        
        # --- CREAR ADMIN POR DEFECTO ---
        print("👤 Verificando usuario administrador...")
        cursor.execute("SELECT id FROM usuarios WHERE correo = %s", ('admin@gmail.com',))
        if not cursor.fetchone():
            hashed_password = generate_password_hash('admin123')
            cursor.execute("""
                INSERT INTO usuarios (nombre, correo, edad, contraseña, direccion, rol)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, ('Administrador Principal', 'admin@gmail.com', 30, hashed_password, 'Oficina Central', 'administrador'))
            conn.commit()
            print("✅ Usuario administrador creado: admin@gmail.com / admin123")
        else:
            print("ℹ️ El usuario administrador ya existe")
        
        # Verificar tablas creadas
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """)
        
        tables = cursor.fetchall()
        
        print("✅ Esquema de base de datos creado exitosamente!")
        print(f"\n📊 Tablas creadas:")
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
            count = cursor.fetchone()[0]
            print(f"   ✓ {table[0]}: {count} registros")
        
        cursor.close()
        conn.close()
        
        return True
        
    except psycopg2.Error as e:
        print(f"❌ Error al crear el esquema: {e}")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Inicializando base de datos PostgreSQL...")
    print("-" * 60)
    
    if create_schema():
        print("\n✅ ¡Base de datos lista para usar!")
        print("💡 Ahora puedes ejecutar tu aplicación Flask")
    else:
        print("\n❌ Hubo un error al crear la base de datos")
        print("💡 Verifica que DATABASE_URL esté configurada correctamente")
