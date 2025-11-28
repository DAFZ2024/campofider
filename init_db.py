"""
Script para inicializar la base de datos SQLite3
Ejecuta este archivo para crear la base de datos con todas las tablas y datos
"""
import sqlite3
import os

# Ruta de la base de datos
DB_PATH = 'usuariosdb.db'
SQL_FILE = 'usuariosdb.sql'

def init_database():
    """Crea la base de datos SQLite3 desde el archivo SQL"""
    
    # Verificar si el archivo SQL existe
    if not os.path.exists(SQL_FILE):
        print(f"❌ Error: No se encontró el archivo {SQL_FILE}")
        return False
    
    try:
        # Conectar a la base de datos (se crea si no existe)
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Leer el archivo SQL
        with open(SQL_FILE, 'r', encoding='utf-8') as f:
            sql_script = f.read()
        
        # Ejecutar el script SQL
        cursor.executescript(sql_script)
        
        # Confirmar cambios
        conn.commit()
        
        # Verificar que las tablas se crearon
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        print("✅ Base de datos creada exitosamente!")
        print(f"📁 Ubicación: {os.path.abspath(DB_PATH)}")
        print(f"\n📊 Tablas creadas:")
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
            count = cursor.fetchone()[0]
            print(f"   - {table[0]}: {count} registros")
        
        conn.close()
        return True
        
    except sqlite3.Error as e:
        print(f"❌ Error al crear la base de datos: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Inicializando base de datos SQLite3...")
    print("-" * 50)
    init_database()
