"""
Script de migración para agregar columnas de estadísticas en vivo a la tabla reservas
Este script se ejecuta automáticamente en Railway después de init_db_postgres.py
"""
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def migrate_reservas():
    """Agrega las columnas de estadísticas en vivo a la tabla reservas"""
    
    database_url = os.getenv('DATABASE_URL')
    
    if not database_url:
        print("❌ Error: DATABASE_URL no está configurada")
        return False
    
    database_url = database_url.strip()
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    
    try:
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        
        print("🔄 Migrando tabla reservas...")
        
        # Lista de columnas a agregar
        columns_to_add = [
            ("goles_equipo1", "INTEGER DEFAULT 0"),
            ("goles_equipo2", "INTEGER DEFAULT 0"),
            ("tarjetas_amarillas", "INTEGER DEFAULT 0"),
            ("tarjetas_rojas", "INTEGER DEFAULT 0"),
            ("estado", "VARCHAR(20) DEFAULT 'pendiente'")
        ]
        
        for col_name, col_type in columns_to_add:
            try:
                # Verificar si la columna ya existe
                cursor.execute("""
                    SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_name='reservas' AND column_name=%s
                """, (col_name,))
                
                if cursor.fetchone():
                    print(f"  ℹ️  Columna '{col_name}' ya existe")
                else:
                    # Agregar la columna
                    cursor.execute(f"ALTER TABLE reservas ADD COLUMN {col_name} {col_type}")
                    conn.commit()
                    print(f"  ✅ Columna '{col_name}' agregada exitosamente")
                    
            except psycopg2.Error as e:
                print(f"  ⚠️  Error al agregar columna '{col_name}': {e}")
                conn.rollback()
        
        cursor.close()
        conn.close()
        
        print("✅ Migración completada")
        return True
        
    except Exception as e:
        print(f"❌ Error en la migración: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Ejecutando migración de reservas...")
    print("-" * 60)
    migrate_reservas()
