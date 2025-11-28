"""
Test de conexion a PostgreSQL de Railway (version simplificada para Windows)
"""
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

print("=" * 60)
print("TEST DE CONEXION POSTGRESQL - RAILWAY")
print("=" * 60)
print()

# Obtener DATABASE_URL
database_url = os.getenv('DATABASE_URL')

if not database_url:
    print("[ERROR] No se encontro DATABASE_URL")
    print()
    print("Pasos para solucionar:")
    print("1. Edita el archivo .env")
    print("2. Agrega: DATABASE_URL=tu_url_de_railway")
    print("3. Descomenta: RAILWAY_ENVIRONMENT=production")
    exit(1)

# Convertir formato si es necesario
if database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)
    print("[OK] URL convertida al formato correcto")

# Ocultar contraseña en el log
safe_url = database_url.split('@')[1] if '@' in database_url else 'URL oculta'
print(f"[INFO] Conectando a: ...@{safe_url}")
print()

try:
    import psycopg2
    
    # Intentar conectar
    print("[INFO] Conectando...")
    conn = psycopg2.connect(database_url)
    cursor = conn.cursor()
    
    # Verificar version de PostgreSQL
    cursor.execute("SELECT version();")
    version = cursor.fetchone()[0]
    print("[OK] Conexion exitosa!")
    print(f"[INFO] PostgreSQL Version: {version.split(',')[0]}")
    print()
    
    # Verificar si existen tablas
    cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
        ORDER BY table_name;
    """)
    
    tables = cursor.fetchall()
    
    if tables:
        print(f"[INFO] Tablas existentes ({len(tables)}):")
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
            count = cursor.fetchone()[0]
            print(f"  - {table[0]}: {count} registros")
    else:
        print("[INFO] No hay tablas creadas todavia")
        print("[ACCION] Ejecuta: python init_db_postgres.py")
    
    # Cerrar conexion
    cursor.close()
    conn.close()
    
    print()
    print("=" * 60)
    print("[EXITO] TODO FUNCIONA CORRECTAMENTE!")
    print("[SIGUIENTE] Ejecuta init_db_postgres.py para crear las tablas")
    print("=" * 60)
    
except psycopg2.OperationalError as e:
    print(f"[ERROR] Error de conexion: {e}")
    print()
    print("Posibles causas:")
    print("1. DATABASE_URL incorrecta")
    print("2. Base de datos no accesible")
    print("3. Credenciales incorrectas")
    
except Exception as e:
    print(f"[ERROR] Error inesperado: {e}")
