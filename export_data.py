"""
Script opcional para migrar datos de SQLite a PostgreSQL
Solo ejecuta esto si quieres transferir datos existentes
"""
import sqlite3
import json
from datetime import datetime

def export_data_from_sqlite():
    """Exporta todos los datos de SQLite a un archivo JSON"""
    
    try:
        # Conectar a SQLite
        conn = sqlite3.connect('usuariosdb.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        data = {}
        
        # Tablas a exportar
        tables = ['usuarios', 'canchas', 'favoritos', 'horarios_canchas', 'reservas']
        
        print("📤 Exportando datos de SQLite...")
        print("-" * 60)
        
        for table in tables:
            try:
                cursor.execute(f"SELECT * FROM {table}")
                rows = cursor.fetchall()
                
                # Convertir rows a diccionarios
                data[table] = []
                for row in rows:
                    row_dict = dict(row)
                    # Convertir valores None y fechas a strings
                    for key, value in row_dict.items():
                        if value is None:
                            row_dict[key] = None
                        elif isinstance(value, (datetime,)):
                            row_dict[key] = value.isoformat()
                    data[table].append(row_dict)
                
                print(f"   ✓ {table}: {len(rows)} registros exportados")
            except sqlite3.Error as e:
                print(f"   ⚠️  {table}: No se pudo exportar ({e})")
                data[table] = []
        
        # Guardar a JSON
        with open('data_export.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        conn.close()
        
        print("\n✅ Datos exportados exitosamente a 'data_export.json'")
        print("💡 Ahora puedes usar import_data.py para importar a PostgreSQL")
        return True
        
    except Exception as e:
        print(f"❌ Error al exportar datos: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Exportando datos de SQLite...")
    print("=" * 60)
    export_data_from_sqlite()
